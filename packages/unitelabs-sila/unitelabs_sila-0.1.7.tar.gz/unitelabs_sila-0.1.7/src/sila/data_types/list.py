from __future__ import annotations

import dataclasses
import io
import typing

from sila import protobuf

from .data_type import DataType


@dataclasses.dataclass
class List(DataType[list]):
    """The SiLA list type is an ordered list with entries of the same SiLA data type."""

    data_type: DataType = dataclasses.field(default_factory=DataType)

    def encode(self, value: list, field_number: int = 1) -> bytes:
        stream = io.BytesIO()
        for item in value:
            data = self.data_type.encode(item, field_number=field_number)

            protobuf.Tag(field_number=field_number, wire_type=protobuf.WireType.LEN).write_to(stream)
            protobuf.write_unsigned_varint(protobuf.uint(len(data)), stream)
            stream.write(data)

        return stream.getvalue()

    def decode(self, data: bytes) -> list:
        stream = io.BytesIO(data)
        values: list[typing.Any] = []
        while True:
            try:
                protobuf.Tag.read_from(stream)
            except EOFError:
                break
            else:
                size = protobuf.read_unsigned_varint(stream)
                payload = stream.read(size)

                value = self.data_type.decode(payload)
                values.append(value)

        return values
