"""Module for DataFrame JSON serialization."""

import datetime
import re
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import cast

import numpy as np
import orjson
import pandas as pd
from pandas.api.types import infer_dtype

SCHEMA_VERSION = "0.1.0"
SCHEMA_ID = "storage_schema"
PERIOD_REGEX = re.compile(r"period\[([A-Z\-]+)\]")
DATETIME_REGEX = re.compile(r"datetime(?:64)?(?:\[([a-zA-Z]+)(?:,\s*(.*))?\])?")
INDEX_NAME = "__index"


class IncompatibleSchemaError(TypeError):
    """The DataFrame being deserialized does not match the current schema version."""

    def __init__(self, schema_version: str, *args: object) -> None:
        """Initialize exception."""
        super().__init__(
            f"DataFrame schema version ({schema_version}) "
            f"is incompatible with the current version ({SCHEMA_VERSION}).",
            *args,
        )


def _collect_fields(data: pd.DataFrame) -> List[Dict[str, str]]:
    # KNOWN ISSUE: str(name) must be replaced with a better fix
    fields = []
    for name, ty in zip(data, map(str, data.dtypes)):
        if data[name].empty:
            # handle a DataFrame with columns but no rows
            fields.append({"name": str(name), "type": ty})
        elif ty == "object":
            # datetime.date and datetime.time are inferred as date and time respectively
            fields.append({"name": str(name), "type": infer_dtype(data[name])})
        elif ty.startswith(("period", "datetime64")):
            fields.append({"name": str(name), "type": ty})

    return fields


def _prepare_dataframe(data: pd.DataFrame) -> Tuple[Dict[str, Any], pd.DataFrame]:
    data = data.copy(deep=True)
    schema = build_schema(data)
    data.index.name = INDEX_NAME

    if not data.empty:
        data = _sort_dataframe(data)

    if schema["index"]["type"].startswith("period"):
        data.index = data.index.to_timestamp()

    data.reset_index(inplace=True)

    for field in schema["fields"]:
        if field["type"].startswith("period"):
            data[field["name"]] = data[field["name"]].dt.to_timestamp()

    return schema, data


def _sort_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    if (
        pd.api.types.is_datetime64_any_dtype(data.index)
        or pd.api.types.is_period_dtype(data.index)
        or isinstance(data.index[0], datetime.date)
        or (
            pd.api.types.is_integer_dtype(data.index) and int(data.index[0]) > 1_000_000
        )
    ):
        data.sort_index(ascending=True, inplace=True)

    return data


def _setup_index(schema: Dict[str, Any], dataframe: pd.DataFrame) -> None:
    if "index" not in schema:
        return

    idx = schema["index"]
    data = dataframe.get(INDEX_NAME, [])

    if idx["type"] == "category":
        dataframe[INDEX_NAME] = pd.CategoricalIndex(data=data)

    elif idx["type"].startswith("period"):
        dataframe[INDEX_NAME] = pd.PeriodIndex(
            data=pd.to_datetime(data, unit="ms"), dtype=idx["type"]
        )

    elif idx["type"] == "time":
        dataframe[INDEX_NAME] = pd.to_datetime(data).dt.time

    elif idx["type"] == "date":
        dataframe[INDEX_NAME] = pd.to_datetime(data, unit="ms").dt.date

    elif (dt_match := DATETIME_REGEX.match(idx["type"])) is not None:
        _, tz = cast(Tuple[Optional[str], ...], dt_match.groups())

        dataframe[INDEX_NAME] = pd.DatetimeIndex(
            data=pd.to_datetime(data, unit="ms"),
            freq=idx.get("freq"),
        )

        if tz is not None:
            dataframe[INDEX_NAME] = (
                dataframe[INDEX_NAME]
                .dt.tz_localize(datetime.timezone.utc)
                .dt.tz_convert(tz)
            )

    elif dataframe.empty:
        dataframe[INDEX_NAME] = []

    dataframe.set_index(INDEX_NAME, drop=True, inplace=True)
    dataframe.index.name = idx["name"]


def _convert_columns(schema: Dict[str, Any], df: pd.DataFrame) -> None:
    for field in schema["fields"]:
        ty = field["type"]
        name = field["name"]

        # If the column does not exist, create it
        if name not in df:
            df[name] = []

        # Handle the column conversion
        if ty == "date":
            df[name] = pd.to_datetime(df[name], unit="ms").dt.date
        elif ty == "time":
            df[name] = pd.to_datetime(df[name]).dt.time
        elif (period_match := PERIOD_REGEX.match(ty)) is not None:
            df[name] = pd.to_datetime(df[name], unit="ms").dt.to_period(
                period_match.groups()[0]
            )
        elif (dt_match := DATETIME_REGEX.match(ty)) is not None:
            _, tz = cast(Tuple[Optional[str], ...], dt_match.groups())

            if tz is not None:
                df[name] = (
                    pd.to_datetime(df[name], unit="ms")
                    .dt.tz_localize(datetime.timezone.utc)
                    .dt.tz_convert(tz)
                )
            else:
                # if not UTC, will probably fail
                df[name] = pd.to_datetime(df[name], unit="ms")


def _check_schema_compatibility(schema: Dict[str, Any]) -> None:
    # basic check, once the schema is stable we can do a more elaborate check
    if (v := schema["version"]) != SCHEMA_VERSION:
        raise IncompatibleSchemaError(v)


def build_schema(data: pd.DataFrame) -> Dict[str, Any]:
    """Build a custom schema for a :class:`pandas.DataFrame`.

    Supports the following indexes:
    * :class:`pandas.CategoricalIndex`
    * :class:`pandas.Int64Index`
    * :class:`pandas.UInt64Index`
    * :class:`pandas.Float64Index`
    * :class:`pandas.DatetimeIndex`
    * :class:`pandas.PeriodIndex`

    Unsupported:
    * :class:`pandas.RangeIndex`

    Args:
        data (pandas.DataFrame): the target :class:`pandas.DataFrame`.

    Returns:
        Dict[str, Any]: the resulting schema.
    """
    idx = data.index
    index = {
        "name": idx.name,
        "type": infer_dtype(idx) if idx.dtype == np.dtype("O") else str(idx.dtype),
    }
    if isinstance(idx, pd.DatetimeIndex) and idx.freqstr is not None:
        index["freq"] = idx.freqstr

    return {
        "version": SCHEMA_VERSION,
        "index": index,
        "fields": _collect_fields(data),
    }


def from_records(records: List[Dict[str, Any]], schema: Dict[str, Any]) -> pd.DataFrame:
    """Convert a schema and list of records into a DataFrame."""
    _check_schema_compatibility(schema)
    data = pd.DataFrame.from_records(records)
    _convert_columns(schema, data)
    _setup_index(schema, data)
    return data


def to_records(data: pd.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Convert a DataFrame into a schema compliant dictionary."""
    schema, df = _prepare_dataframe(data)

    # certain objects are not serializable by normal json...
    records = orjson.loads(df.to_json(orient="records"))

    return records, schema
