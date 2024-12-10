from __future__ import annotations
from typing_extensions import TypeAlias, Mapping, TypeIs, Any

Number: TypeAlias = int | float

JsonValueType: TypeAlias = Number | str | bool | None
JsonArray: TypeAlias = list["JsonElementType"] | tuple["JsonElementType", ...]
JsonObject: TypeAlias = Mapping[str, "JsonElementType"]
JsonRootType: TypeAlias = JsonArray | JsonObject
JsonElementType: TypeAlias = JsonRootType | JsonValueType

Json: TypeAlias = JsonRootType

SimpleJson: TypeAlias = Mapping[str, JsonValueType]


def is_number(value: Any) -> TypeIs[Number]:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_json_value(value: Any) -> TypeIs[JsonValueType]:
    return is_number(value) or isinstance(value, (str, bool)) or value is None


def is_json_array(value: Any) -> TypeIs[JsonArray]:
    if isinstance(value, (list, tuple)):
        valuelist: list[Any] = list(value)  # type: ignore[assignment]
        return all(is_json_element(item) for item in valuelist)
    return False


def is_json_object(value: Any) -> TypeIs[JsonObject]:
    if isinstance(value, dict):
        valuedict: dict[Any, Any] = value
        return all(
            isinstance(key, str) and is_json_element(val)
            for key, val in valuedict.items()
        )
    return False


def is_json_root(value: Any) -> TypeIs[JsonRootType]:
    return is_json_array(value) or is_json_object(value)


is_json = is_json_root


def is_json_element(value: Any) -> TypeIs[JsonElementType]:
    return is_json_root(value) or is_json_value(value)


def is_simple_json(value: Any) -> TypeIs[SimpleJson]:
    if not isinstance(value, dict):
        return False
    for value_item in value.values():  # type: ignore
        if not is_json_value(value_item):
            return False
    return True
