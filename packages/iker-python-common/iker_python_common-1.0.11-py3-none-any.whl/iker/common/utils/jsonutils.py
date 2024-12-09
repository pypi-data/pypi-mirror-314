import math
from collections.abc import Callable, Mapping, Sequence, Set
from typing import Any, SupportsFloat, SupportsInt

from iker.common.utils.numutils import is_normal_real

__all__ = [
    "JsonKey",
    "JsonValue",
    "JsonArray",
    "JsonObject",
    "JsonType",
    "JsonKeyCompatible",
    "JsonValueCompatible",
    "JsonArrayCompatible",
    "JsonObjectCompatible",
    "JsonTypeCompatible",
    "NodePath",
    "json_traverse",
    "json_reformat",
    "json_sanitize",
    "json_compare",
]

JsonKey = str
JsonValue = str | bool | float | int | None
JsonObject = dict[JsonKey, "JsonType"]
JsonArray = list["JsonType"]
JsonType = JsonValue | JsonObject | JsonArray

JsonKeyCompatible = str
JsonValueCompatible = str | bool | SupportsFloat | SupportsInt | None
JsonObjectCompatible = Mapping[JsonKeyCompatible, "JsonTypeCompatible"]
JsonArrayCompatible = Sequence["JsonTypeCompatible"]
JsonTypeCompatible = JsonValueCompatible | JsonObjectCompatible | JsonArrayCompatible

NodePath = list[str | int]


def default_key_visitor(node_path: NodePath, key: JsonKeyCompatible) -> JsonKey:
    return str(key)


def default_value_visitor(node_path: NodePath, value: JsonValueCompatible) -> JsonValue:
    if value is None or isinstance(value, JsonValue):
        return value
    if isinstance(value, SupportsFloat):
        return float(value)
    if isinstance(value, SupportsInt):
        return int(value)
    raise ValueError(f"unsupported type '{type(value)}' encountered")


def default_object_visitor(node_path: NodePath, old_object: JsonObjectCompatible, new_object: JsonObject) -> JsonType:
    return new_object


def default_array_visitor(node_path: NodePath, old_array: JsonArrayCompatible, new_array: JsonArray) -> JsonType:
    return new_array


def json_traverse(
    obj: Any,
    key_visitor: Callable[[NodePath, JsonKeyCompatible], JsonKey] = default_key_visitor,
    value_visitor: Callable[[NodePath, JsonValueCompatible], JsonType] = default_value_visitor,
    object_visitor: Callable[[NodePath, JsonObjectCompatible, JsonObject], JsonType] = default_object_visitor,
    array_visitor: Callable[[NodePath, JsonArrayCompatible, JsonArray], JsonType] = default_array_visitor,
    stop_func: Callable[[NodePath], bool] = lambda x: False,
    *,
    raise_if_unregistered: bool = True,
    unregistered_visitor: Callable[[NodePath, Any], JsonType] | None = None,
) -> JsonType:
    def func(obj: Any, node_path: NodePath):
        if stop_func(node_path):
            return None
        if obj is None or isinstance(obj, (JsonValue | JsonValueCompatible)):
            return value_visitor(node_path, obj)
        if isinstance(obj, Mapping):
            return object_visitor(
                node_path,
                obj,
                {key_visitor(node_path, key): func(value, node_path + [key]) for key, value in obj.items()},
            )
        if isinstance(obj, Sequence):
            return array_visitor(
                node_path,
                obj,
                [func(item, node_path + [index]) for index, item in enumerate(obj)],
            )
        if raise_if_unregistered or unregistered_visitor is None:
            raise ValueError(f"unregistered type '{type(obj)}' encountered")
        return unregistered_visitor(node_path, obj)

    return func(obj, [])


def default_key_formatter(key: JsonKeyCompatible) -> JsonKey:
    return str(key)


def default_value_formatter(value: JsonValueCompatible) -> JsonValue:
    if value is None or isinstance(value, JsonValue):
        return value
    if isinstance(value, SupportsFloat):
        return float(value)
    if isinstance(value, SupportsInt):
        return int(value)
    raise ValueError(f"unsupported type '{type(value)}' encountered")


def json_reformat(
    obj: Any,
    key_formatter: Callable[[JsonKeyCompatible], JsonKey] = default_key_formatter,
    value_formatter: Callable[[JsonValueCompatible], JsonType] = default_value_formatter,
    *,
    raise_if_unregistered: bool = True,
    unregistered_formatter: Callable[[Any], JsonType] | None = None,
) -> JsonType:
    def key_visitor(node_path: NodePath, key: JsonKeyCompatible) -> JsonKey:
        return key_formatter(key)

    def value_visitor(node_path: NodePath, value: JsonValueCompatible) -> JsonType:
        return value_formatter(value)

    def unregistered_visitor(node_path: NodePath, obj: Any) -> JsonType:
        return unregistered_formatter(obj) if unregistered_formatter is not None else None

    return json_traverse(obj,
                         key_visitor=key_visitor,
                         value_visitor=value_visitor,
                         raise_if_unregistered=raise_if_unregistered,
                         unregistered_visitor=unregistered_visitor)


def json_sanitize(obj: Any, *, str_inf_nan: bool = True, str_unregistered: bool = True) -> JsonType:
    def value_formatter(value: JsonValue) -> JsonValue:
        if isinstance(value, float) and not is_normal_real(value):
            return str(value) if str_inf_nan else None
        return default_value_formatter(value)

    def unregistered_formatter(unregistered: Any) -> JsonType:
        if isinstance(unregistered, Set):
            return [json_sanitize(item, str_inf_nan=str_inf_nan, str_unregistered=str_unregistered)
                    for item in unregistered]
        return str(unregistered) if str_unregistered else None

    return json_reformat(obj,
                         value_formatter=value_formatter,
                         raise_if_unregistered=False,
                         unregistered_formatter=unregistered_formatter)


def json_compare(
    a: JsonType,
    b: JsonType,
    *,
    int_strict: bool = False,
    float_tol: float = 1e-5,
    list_order: bool = True,
    dict_extra: bool = False,
) -> bool:
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, (dict, list, str, bool)):
        if type(a) != type(b):
            return False
        if isinstance(a, dict):
            if not dict_extra and set(a.keys()) != set(b.keys()):
                return False
            return all(json_compare(a[k],
                                    b[k],
                                    int_strict=int_strict,
                                    float_tol=float_tol,
                                    list_order=list_order,
                                    dict_extra=dict_extra)
                       for k in set(a.keys()) & set(b.keys()))
        if isinstance(a, list):
            if len(a) != len(b):
                return False
            if list_order:
                return all(json_compare(va,
                                        vb,
                                        int_strict=int_strict,
                                        float_tol=float_tol,
                                        list_order=list_order,
                                        dict_extra=dict_extra)
                           for va, vb in zip(a, b))
            else:
                return all(json_compare(va,
                                        vb,
                                        int_strict=int_strict,
                                        float_tol=float_tol,
                                        list_order=list_order,
                                        dict_extra=dict_extra)
                           for va, vb in zip(sorted(a), sorted(b)))
        return a == b
    if isinstance(a, (float, int)) and isinstance(b, (float, int)):
        if int_strict:
            if type(a) != type(b):
                return False
        if isinstance(a, float) or isinstance(b, float):
            if math.isnan(a) and math.isnan(b):
                return True
            if math.isinf(a) and math.isinf(b):
                return a == b
            return abs(a - b) <= float_tol
        return a == b
    raise ValueError(f"incompatible type '{type(a)}' and '{type(b)}'")
