import typing
from typing import Any
import types
import dataclasses
import inspect


if typing.TYPE_CHECKING:
    from _typeshed import DataclassInstance


class ValidationException(Exception):
    pass


def normalize_generic_list(arg: type, data: list[Any]) -> list[Any]:
    for i, val in enumerate(data):
        if isinstance(arg, types.GenericAlias):
            data[i] = normalize_generic(arg, val)
            arg = typing.get_origin(arg)
        if dataclasses.is_dataclass(arg):
            data[i] = unpack(val, arg)

        if not isinstance(data[i], arg):
            raise ValidationException(
                f"Field `{data[i]}` is not an instance of `{arg}`!"
            )

    return data


def normalize_generic_dict(
    args: tuple[type, ...], data: dict[str, Any]
) -> dict[str, Any]:
    for key, val in data.items():
        if dataclasses.is_dataclass(args[1]):
            data[key] = unpack(val, args[1])

        if not isinstance(key, args[0]):
            raise ValidationException(
                f"Field `{key}` is not an instance of `{args[0]}`!"
            )
        if not isinstance(data[key], args[1]):
            raise ValidationException(
                f"Field `{data[key]}` is not an instance of `{args[1]}`!"
            )

    return data


def normalize_generic[D: (list[Any], dict[str, Any])](
    t: types.GenericAlias, data: D
) -> D:
    args = typing.get_args(t)

    if isinstance(data, list):
        return normalize_generic_list(args[0], data)

    elif isinstance(data, dict):
        return normalize_generic_dict(args, data)


def unpack[S: DataclassInstance](data: dict[str, Any], structure: type[S]) -> S:
    unpacked = {}
    annotations = inspect.get_annotations(structure)

    resolved_type_hints = typing.get_type_hints(structure)

    for field in dataclasses.fields(structure):
        alias = field.metadata.get("name", field.name)

        # It's necessary to use the resolved type hints from `typing.get_type_hints()` in order to
        # satisfy mypy. We could use `field.type`, but that could be a `str`.
        field_type = resolved_type_hints[field.name]

        if dataclasses.is_dataclass(annotations[field.name]):
            unpacked[field.name] = unpack(data[alias], field_type)

        elif isinstance(field_type, types.GenericAlias):
            unpacked[field.name] = normalize_generic(field_type, data[alias])

        elif isinstance(data[alias], field_type):
            unpacked[field.name] = data[alias]

        else:
            raise ValidationException(
                f"Field `{field.name}` should be `{field_type.__name__}`, found `{type(data[alias]).__name__}`!"
            )

    return structure(**unpacked)
