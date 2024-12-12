from __future__ import annotations

import dataclasses
import datetime
import typing

from sila import protobuf

from .basic_type import BasicType


@dataclasses.dataclass
class Timezone(BasicType[datetime.timezone]):
    """
    The SiLA timezone type represents a signed, fixed-length span of time represented as a count of hours and minutes as
    an offset from UTC. This is used for the SiLA date type, the SiLA timestamp type and the SiLA time type which all
    need to provide a timezone.
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA timezone type."""

        hours: typing.Annotated[int, protobuf.Field(1)] = 0
        minutes: typing.Annotated[protobuf.uint, protobuf.Field(2)] = protobuf.uint(0)

    @classmethod
    def from_native(cls, value: datetime.timezone) -> Timezone.Message:
        offset = value.utcoffset(None)
        hours, minutes = divmod(offset.total_seconds() // 60, 60)

        return Timezone.Message(hours=int(hours), minutes=protobuf.uint(int(minutes)))

    @classmethod
    def to_native(cls, message: Timezone.Message) -> datetime.timezone:
        return datetime.timezone(offset=datetime.timedelta(hours=message.hours, minutes=message.minutes))
