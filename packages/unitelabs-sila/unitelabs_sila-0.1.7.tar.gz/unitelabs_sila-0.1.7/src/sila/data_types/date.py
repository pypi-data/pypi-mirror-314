from __future__ import annotations

import dataclasses
import typing

from sila import datetime, protobuf

from .basic_type import BasicType
from .timezone import Timezone


@dataclasses.dataclass
class Date(BasicType[datetime.date]):
    """
    The SiLA date type represents an ISO 8601 date (year [1-9999]), month [1-12], day [1-31]) in the Gregorian calendar,
    with an additional timezone (as an offset from UTC). A SiLA date type consists of the top-open interval of exactly
    one day in length, beginning on the beginning moment of each day (in each timezone), i.e. '00:00:00', up to but not
    including '24:00:00' (which is identical with '00:00:00' of the next day).
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA date type."""

        year: typing.Annotated[protobuf.uint, protobuf.Field(3)] = protobuf.uint(0)
        month: typing.Annotated[protobuf.uint, protobuf.Field(2)] = protobuf.uint(0)
        day: typing.Annotated[protobuf.uint, protobuf.Field(1)] = protobuf.uint(0)
        timezone: typing.Annotated[Timezone.Message, protobuf.Field(4)] = dataclasses.field(
            default_factory=Timezone.Message
        )

    @classmethod
    def from_native(cls, value: datetime.date) -> Date.Message:
        return Date.Message(
            year=protobuf.uint(value.year),
            month=protobuf.uint(value.month),
            day=protobuf.uint(value.day),
            timezone=Timezone.from_native(
                datetime.timezone(offset)
                if value.tzinfo and (offset := value.tzinfo.utcoffset(None))
                else datetime.timezone.utc
            ),
        )

    @classmethod
    def to_native(cls, message: Date.Message) -> datetime.date:
        return datetime.date(
            year=int(message.year),
            month=int(message.month),
            day=int(message.day),
            tzinfo=Timezone.to_native(message.timezone),
        )
