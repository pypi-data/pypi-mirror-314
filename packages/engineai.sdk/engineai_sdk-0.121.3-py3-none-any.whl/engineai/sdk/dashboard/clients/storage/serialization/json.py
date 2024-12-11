"""Serialization utils."""

import logging
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union
from typing import cast

import orjson
import pandas as pd

from engineai.sdk.dashboard.clients.storage.serialization import dataframe

logger = logging.getLogger(__name__)


JSONType = TypeVar("JSONType", bool, int, float, str, List[Any], Dict[str, Any], None)
"""JSON value types."""


def serialize(value: Union[pd.DataFrame, JSONType]) -> Tuple[bytes, Optional[bytes]]:
    """Serializes a value.

    Arguments:
        value (Union[pd.DataFrame, JSONType]): The value to be serialized.

    Returns:
        Tuple[bytes, Optional[bytes]]: Tuple with the serialized value and the
            serialized value's schema. Only serialized dataframes returns a schema.
    """
    if isinstance(value, pd.DataFrame):
        records, schema = dataframe.to_records(value)

        return orjson.dumps(records, option=orjson.OPT_SERIALIZE_NUMPY), orjson.dumps(
            schema
        )

    if isinstance(value, dict) and all(
        isinstance(v, pd.DataFrame) for v in value.values()
    ):
        # supoort for Dict[str, pd.DataFrame]
        schemas = {}
        data = {}
        for key, df in value.items():
            records, schema = dataframe.to_records(df)
            schemas[key] = schema
            data[key] = records

        return orjson.dumps(data, option=orjson.OPT_SERIALIZE_NUMPY), orjson.dumps(
            schemas, option=orjson.OPT_SERIALIZE_NUMPY
        )

    return orjson.dumps(value, option=orjson.OPT_SERIALIZE_NUMPY), None


def deserialize(
    value: Union[bytes, str],
    schema: Optional[Union[Callable[[], Optional[bytes]], bytes]] = None,
) -> Union[pd.DataFrame, JSONType]:
    """Deserializes value from bytes.

    Args:
        value (str): Value to be deserialized.
        schema (Optional[Dict[str, Any]]): The value schema, if any. Defaults to `None`.

    Returns:
        Union[pd.DataFrame, JSONType]: The deserialized value.
    """
    logger.info("deserialize value: %s", value)
    deserialized_value = orjson.loads(value)
    if isinstance(deserialized_value, list) and schema is not None:
        serialized_schema = schema if not callable(schema) else schema()
        if serialized_schema is not None:
            return dataframe.from_records(
                deserialized_value, orjson.loads(serialized_schema)
            )

    if isinstance(deserialized_value, dict) and schema is not None:
        # supoort for Dict[str, pd.DataFrame]
        serialized_schema = schema if not callable(schema) else schema()
        if serialized_schema is not None:
            deserialized_schema = orjson.loads(serialized_schema)
            return cast(
                JSONType,
                {
                    key: dataframe.from_records(records, deserialized_schema[key])
                    for key, records in deserialized_value.items()
                },
            )

    return cast(JSONType, deserialized_value)
