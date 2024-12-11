"""Map Value Objects to dictionaries and construct Value Objects from Dictionaries"""

from enum import Enum, EnumType
from dataclasses import MISSING, fields, is_dataclass
from typing import Any, Type, TypeVar, get_args, get_origin
from types import UnionType


T = TypeVar("T")


class PrimitiveMapper:
    """Convert a compatible class to a dictionary with primitive values and
    and construct a object from a primitive dictionary(if a dataclass)"""

    @staticmethod
    def from_primitive(primitive, value_cls):
        if _DataclassMapper.is_dataclass(value_cls):
            return _DataclassMapper.from_primitive_dict(primitive, value_cls)
        elif _ListMapper.is_list(value_cls):
            return _ListMapper.from_primitive_list(primitive, value_cls)
        elif _TupleMapper.is_tuple(value_cls):
            return _TupleMapper.from_primitive_tuple(primitive, value_cls)
        elif _EnumMapper.is_enum(value_cls):
            print("aqui he pasado")
            print(value_cls)
            return _EnumMapper.from_primitive(primitive, value_cls)
        elif _DictMapper.is_dict(value_cls):
            return _DictMapper.from_primitive_dict(primitive, value_cls)

        return primitive

    @staticmethod
    def to_primitive(
        value, enum_as_value: bool = True, exclude_defaults: bool = True
    ) -> dict[str, Any] | list[Any] | tuple[Any, ...] | str | int:
        if _DataclassMapper.is_dataclass(value):
            return _DataclassMapper.to_primitive_dict(
                value, enum_as_value, exclude_defaults
            )
        elif _ListMapper.is_list(value):
            return _ListMapper.to_primitive_list(value, enum_as_value, exclude_defaults)
        elif _TupleMapper.is_tuple(value):
            return _TupleMapper.to_primitive_tuple(
                value, enum_as_value, exclude_defaults
            )
        elif _EnumMapper.is_enum(value):
            return _EnumMapper.to_primitive(value, enum_as_value)
        elif _DictMapper.is_dict(value):
            return _DictMapper.to_primitive_dict(value, enum_as_value, exclude_defaults)

        return value


class _EnumMapper:
    @staticmethod
    def is_enum(value):
        return isinstance(value, Enum) or (type(value) is EnumType)

    @staticmethod
    def from_primitive(
        value: str | int,
        enum_class: Type[Enum],
    ) -> Enum:
        if type(value) is str:
            return enum_class[value]
        elif type(value) is int:
            return enum_class(value)
        raise ValueError(f"Argument for creating a enum shall be string or integer")

    @staticmethod
    def to_primitive(value: Enum, enum_to_value: bool):
        if enum_to_value:
            return value.value
        return value.name


class _ListMapper:
    @staticmethod
    def is_list(value):
        return type(value) is list or get_origin(value) is list

    @staticmethod
    def from_primitive_list(value: list[Any], value_cls) -> list:
        return [
            PrimitiveMapper.from_primitive(item, get_args(value_cls)[0])
            for item in value
        ]

    @staticmethod
    def to_primitive_list(
        value: list[Any], enum_to_value: bool, exclude_defaults: bool
    ):
        return [
            PrimitiveMapper.to_primitive(item, enum_to_value, exclude_defaults)
            for item in value
        ]


class _TupleMapper:
    @staticmethod
    def is_tuple(value):
        return type(value) is tuple or get_origin(value) is tuple

    @staticmethod
    def from_primitive_tuple(value: tuple[Any, ...], value_cls) -> tuple:
        return tuple(
            [
                PrimitiveMapper.from_primitive(item, get_args(value_cls)[0])
                for item in value
            ]
        )

    @staticmethod
    def to_primitive_tuple(
        value: tuple[Any], enum_to_value: bool, exclude_defaults: bool
    ):
        return tuple(
            [
                PrimitiveMapper.to_primitive(item, enum_to_value, exclude_defaults)
                for item in value
            ]
        )


class _DictMapper:
    @staticmethod
    def is_dict(value):
        return type(value) is dict or get_origin(value) is dict

    @staticmethod
    def from_primitive_dict(value: dict[str, Any], value_cls) -> dict:
        return {
            key: PrimitiveMapper.from_primitive(item, get_args(value_cls)[1])
            for key, item in value.items()
        }

    @staticmethod
    def to_primitive_dict(
        value: dict[str, Any], enum_to_value: bool, exclude_defaults: bool
    ):
        return {
            key: PrimitiveMapper.to_primitive(item, enum_to_value, exclude_defaults)
            for key, item in value.items()
        }


class _DataclassMapper:
    """Parse dataclass objects to primitive dictionaries and construct from them"""

    @staticmethod
    def is_dataclass(value_cls: type):
        return is_dataclass(value_cls)

    @staticmethod
    def to_primitive_dict(
        value: Any, enum_to_value: bool = True, exclude_defaults: bool = True
    ) -> dict[str, Any]:
        """Convert a Value object to a jsonable dict"""
        result = {}
        for field in fields(value):
            value_ = getattr(value, field.name)
            if value_ != field.default and (
                field.default_factory is MISSING or value_ != field.default_factory()
            ):
                result[field.name] = PrimitiveMapper.to_primitive(
                    value_, enum_to_value, exclude_defaults
                )
        return result

    @staticmethod
    def from_primitive_dict(data: dict[str, Any], value_cls: Any):
        """Construct a Value object from a primitive dict"""

        def _is_nullable(field_type) -> bool:
            return (
                get_origin(field_type) is UnionType
                and len(get_args(field_type)) == 2
                and get_args(field_type)[1] is type(None)
            )

        init_values = {}
        for field in fields(value_cls):
            if field.name in data:
                print(field.type)
                field_type = (
                    field.type
                    if not _is_nullable(field.type)
                    else get_args(field.type)[0]
                )
                init_values[field.name] = PrimitiveMapper.from_primitive(
                    data[field.name], field_type
                )
            else:
                if field.default is not MISSING:
                    init_values[field.name] = field.default
                elif field.default_factory is not MISSING:  # Handle default_factory
                    init_values[field.name] = field.default_factory()
                else:
                    raise ValueError(
                        f"Field {field.name} is missing and has no default value."
                    )

        return value_cls(**init_values)
