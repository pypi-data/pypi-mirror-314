from __future__ import annotations

import dataclasses
import typing

from sila import protobuf

from .basic_type import BasicType


@dataclasses.dataclass
class Real(BasicType[float]):
    """
    The SiLA real type represents a real number as defined per IEEE 754 double-precision floating-point number.
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA real type."""

        value: typing.Annotated[protobuf.double, protobuf.Field(1)] = protobuf.double(0)

    @classmethod
    def from_native(cls, value: float) -> Real.Message:
        return Real.Message(value=protobuf.double(value))

    @classmethod
    def to_native(cls, message: Real.Message) -> float:
        return float(message.value)
