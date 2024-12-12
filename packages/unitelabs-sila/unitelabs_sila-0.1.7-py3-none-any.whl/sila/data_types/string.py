from __future__ import annotations

import dataclasses
import typing

from sila import protobuf

from .basic_type import BasicType

MAX_LENGTH = 2**21


@dataclasses.dataclass
class String(BasicType[str]):
    """
    The SiLA string type represents a plain text composed of maximum 2 x 2²⁰ unicode characters. Use the SiLA binary
    type for larger data. It is recommended to specify a Constraint, e.g. a content-type constraint or schema constraint
    for the SiLA string type in order to make the string content type safe.
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA string type."""

        value: typing.Annotated[str, protobuf.Field(1)] = ""

    @classmethod
    def from_native(cls, value: str) -> String.Message:
        return String.Message(value=value)

    @classmethod
    def to_native(cls, message: String.Message) -> str:
        return message.value

    def validate(self, value: str) -> None:
        super().validate(value)

        if len(value) > MAX_LENGTH:
            raise ValueError(f"String too long ({len(value)}, allowed: 2 x 2²⁰ characters)")
