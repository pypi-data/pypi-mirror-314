from __future__ import annotations

import dataclasses
import typing

from sila import protobuf

from .basic_type import BasicType


@dataclasses.dataclass
class Binary(BasicType[bytes]):
    """
    The SiLA binary type represents arbitrary binary data of any size such as images, office files, etc. If the SiLA
    binary type is used for character data, e.g. plain text, XML or JSON, the character encoding must be UTF-8. It is
    recommended to specify a constraint, e.g. a content-type constraint or schema constraint for the SiLA binary type in
    order to make the binary content type safe.
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA binary type."""

        union: typing.ClassVar[protobuf.OneOf] = protobuf.OneOf()
        which_one = union.which_one_of_getter()

        value: typing.Annotated[typing.Optional[bytes], protobuf.Field(1)] = None
        binary_transfer_uuid: typing.Annotated[typing.Optional[str], protobuf.Field(2)] = None

    @classmethod
    def from_native(cls, value: bytes) -> Binary.Message:
        return Binary.Message(value=value)

    @classmethod
    def to_native(cls, message: Binary.Message) -> bytes:
        if message.value is not None:
            return message.value

        raise NotImplementedError("Binary IDs are not yet supported")
