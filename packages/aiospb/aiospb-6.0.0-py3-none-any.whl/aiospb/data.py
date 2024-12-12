from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Self, TypeAlias


class Quality(Enum):
    BAD = 0
    GOOD = 192
    STALE = 500


ValueType: TypeAlias = bool | int | float | str | bytes | None


class DataType(Enum):
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14
    UUID = 15
    DataSet = 16
    Bytes = 17
    File = 18
    Template = 19
    PropertySet = 20
    PropertySetList = 21
    Int8Array = 22
    Int16Array = 23
    Int32Array = 24
    Int64Array = 2
    UInt8Array = 26
    UInt16Array = 27
    UInt32Array = 28
    UInt64Array = 29
    FloatArray = 30
    DoubleArray = 31
    BooleanArray = 32
    StringArray = 33
    DateTimeArray = 34

    @classmethod
    def for_(cls, value: ValueType) -> Self:
        v_type = type(value)
        if v_type not in _DEFAULT_DTs:
            raise ValueError(f"There is no default for type {v_type}")
        return _DEFAULT_DTs[v_type]

    def convert_value(self, str_value: str) -> ValueType:
        if str_value == "None":
            return

        if "Int" in self.name:
            return int(str_value)

        if "Float" in self.name or "Double" in self.name:
            return float(str_value)

        if "Boolean" == self.name:
            return str_value == True

        if "Bytes" == self.name:
            return str_value.encode()

        return str_value


_DEFAULT_DTs = {
    int: DataType.Int64,
    float: DataType.Float,
    bool: DataType.Boolean,
    str: DataType.String,
    bytes: DataType.Bytes,
}


@dataclass(frozen=True)
class PropertyValue:
    value: ValueType
    data_type: DataType

    def to_dict(self) -> dict[str, ValueType]:
        return {"value": self.value, "dataType": self.data_type.name}

    @classmethod
    def from_dict(cls, dump: dict[str, Any]) -> Self:
        datatype = (
            DataType[dump["dataType"]]
            if type(dump["dataType"]) is str
            else DataType(dump["dataType"])
        )
        return cls(dump["value"], datatype)

    @classmethod
    def from_value(cls, value: ValueType) -> Self:
        value_type = type(value)
        if value_type not in cls._DEFAULTS:
            raise ValueError(f"Not default for type {type(value)}")

        datatype = cls._DEFAULTS[value_type]

        return cls(value, datatype)


@dataclass(frozen=True)
class PropertySet:
    """Map or properties"""

    keys: tuple[str, ...] = field(default_factory=tuple)
    values: tuple[PropertyValue, ...] = field(default_factory=tuple)

    def __contains__(self, key: str) -> bool:
        return key in self.keys

    def __getitem__(self, key: str) -> PropertyValue:
        try:
            index = self.keys.index(key)
        except ValueError:
            raise KeyError(f"Key {key} not found in properties")

        return self.values[index]

    def __bool__(self) -> bool:
        return bool(self.keys)

    @classmethod
    def from_dict(cls, dump: dict[str, Any]) -> Self:
        """Construct a property set from a dict"""
        keys = tuple(sorted(dump.keys()))
        return cls(keys, tuple([PropertyValue.from_dict(dump[key]) for key in keys]))

    @classmethod
    def from_kwargs(cls, **kwargs) -> Self:
        """Construct property set from keywords arguments"""
        keys = tuple(sorted(kwargs.keys()))

        return cls(keys, tuple([kwargs[key] for key in keys]))

    def as_dict(self) -> dict[str, dict[str, Any]]:
        """Convert object to a dict"""
        return {key: value.to_dict() for key, value in zip(self.keys, self.values)}


@dataclass
class Metric:
    """Data Transfer Object (dto) to be included in Sparkplug Messages"""

    timestamp: int
    value: ValueType
    datatype: DataType
    alias: int = 0
    name: str = ""
    properties: PropertySet = field(default_factory=PropertySet)
    is_transient: bool = False
    is_historical: bool = False

    @classmethod
    def from_dict(cls, dump: dict[str, Any]) -> Self:
        """Construct dto from a dict"""
        return cls(
            dump["timestamp"],
            dump["value"],
            DataType[dump["dataType"]],
            dump.get("alias", 0),
            dump.get("name", ""),
            PropertySet.from_dict(dump.get("properties", {})),
            dump.get("is_transient", False),
            dump.get("is_historical", False),
        )

    def as_dict(self) -> dict[str, Any]:
        """Convert dto to dict for parsing"""
        dump = {
            "timestamp": self.timestamp,
            "value": self.value,
            "dataType": self.datatype.name,
        }
        if self.alias:
            dump["alias"] = self.alias

        if self.name:
            dump["name"] = self.name

        if self.is_transient:
            dump["is_transient"] = True

        if self.properties:
            dump["properties"] = self.properties.as_dict()

        if self.is_historical:
            dump["is_historical"] = True
        return dump


@dataclass(frozen=True)
class WriteRequest:
    value: ValueType
    metric_name: str = ""
    alias: int = 0
