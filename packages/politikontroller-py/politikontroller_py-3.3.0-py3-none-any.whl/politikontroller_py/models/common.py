from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, TypeVar

from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin

from politikontroller_py.utils import map_response_data, unmap_response_data

T = TypeVar("T", bound="DataClassORJSONMixin")


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def from_str(cls, value: str) -> StrEnum:
        return cls(value)

    def __eq__(self, other: str) -> bool:
        return super().__eq__(other)

    def __hash__(self):
        return hash(self.value)


@dataclass
class BaseModel(DataClassORJSONMixin):
    class Config(BaseConfig):
        omit_none = True
        allow_deserialization_not_by_alias = True
        serialize_by_alias = True


@dataclass
class PolitiKontrollerResponse(BaseModel):
    attr_map: ClassVar[list[str]]

    @classmethod
    def from_response_data(cls: T, cvs: str, multiple=False) -> T | list[T]:
        """Convert a cvs-like string into instance(s) of `cls`."""
        data = map_response_data(cvs, cls.attr_map, multiple)
        if multiple:
            return [cls.from_dict(d) for d in data]
        return cls.from_dict(data)

    def to_response_data(self) -> str:  # pragma: no cover
        """Convert a serialized version of `self` into a cvs-like string."""
        return unmap_response_data(self.to_dict(), self.attr_map)
