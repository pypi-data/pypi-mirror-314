from __future__ import annotations

import dataclasses
import typing

from sila import protobuf

from .basic_type import BasicType


@dataclasses.dataclass
class Integer(BasicType[int]):
    """
    The SiLA integer type represents an integer number within a range from the minimum value of -2⁶³ up to a maximum of
    2⁶³ - 1.
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA integer type."""

        value: typing.Annotated[int, protobuf.Field(1)] = 0

    @classmethod
    def from_native(cls, value: int) -> Integer.Message:
        return Integer.Message(value=value)

    @classmethod
    def to_native(cls, message: Integer.Message) -> int:
        return message.value
