from __future__ import annotations

import abc
import dataclasses
import typing

from sila import protobuf

from .data_type import DataType

T = typing.TypeVar("T")


@dataclasses.dataclass
class BasicType(typing.Generic[T], DataType[T], metaclass=abc.ABCMeta):
    """
    The SiLA basic types are predefined data types by SiLA.
    """

    Message: typing.ClassVar[protobuf.BaseMessage]

    @classmethod
    @abc.abstractmethod
    def from_native(cls, value: T) -> protobuf.BaseMessage:
        """Serializes a native python type into a protobuf message."""

    @classmethod
    @abc.abstractmethod
    def to_native(cls, message: protobuf.BaseMessage) -> T:
        """Deserializes a native python type from a protobuf message."""

    def encode(self, value: T, field_number: int = 1) -> bytes:
        self.validate(value)
        return self.from_native(value).dumps()

    def decode(self, data: bytes) -> T:
        message = self.Message.loads(data)
        value = self.to_native(message)
        self.validate(value)
        return value
