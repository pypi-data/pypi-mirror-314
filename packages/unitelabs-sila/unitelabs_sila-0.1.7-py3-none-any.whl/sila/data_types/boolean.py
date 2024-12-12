from __future__ import annotations

import dataclasses
import typing

from sila import protobuf

from .basic_type import BasicType


@dataclasses.dataclass
class Boolean(BasicType[bool]):
    """
    The SiLA boolean type represents a boolean value. This is a SiLA data type representing one of two possible values,
    usually denoted as true and false.
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA boolean type."""

        value: typing.Annotated[bool, protobuf.Field(1)] = False

    @classmethod
    def from_native(cls, value: bool) -> Boolean.Message:
        return Boolean.Message(value=value)

    @classmethod
    def to_native(cls, message: Boolean.Message) -> bool:
        return message.value
