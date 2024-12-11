"""Spec Card Context Labels."""

import warnings
from typing import Any
from typing import Dict
from typing import Iterable

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import RouteLink
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.widget_dependency import WidgetDependencyValue
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings


@type_check
def build_context_label(
    *,
    label: TemplatedStringItem,
    separator: str = "-",
    prefix: str = "",
    suffix: str = "",
) -> Dict[str, Any]:
    """Method to build Card Context Labels.

    Args:
        label: Card Header label value. Can assume a static label, a single WidgetLink
            or a list of WidgetLink's.
        separator: label separator in case of a List of WidgetLinks
        prefix: prefix value to use in before each label.
        suffix: suffix value to use in after each label.
    """
    if isinstance(label, str):
        if prefix or suffix:
            warnings.warn(
                "You don't need to specify `prefix` or "
                "`suffix` when using string as label. You can use them"
                "directly in the `label`."
            )
        value = f"{prefix}{label}{suffix}"

        return {
            "templated": None,
            "dependencyValue": None,
            "stringValue": {"value": value},
        }
    if isinstance(label, WidgetField):
        return {
            "templated": None,
            "dependencyValue": WidgetDependencyValue(widget_field=label).build(),
            "stringValue": None,
        }
    if isinstance(label, (Iterable, RouteLink)):
        return {
            "templated": build_templated_strings(
                items=label, separator=separator, prefix=prefix, suffix=suffix
            ),
            "dependencyValue": None,
            "stringValue": None,
        }
    msg = "build_context_label label argument has a type not implemented."
    raise NotImplementedError(msg)
