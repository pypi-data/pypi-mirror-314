from __future__ import annotations

import dataclasses
import io
import typing

from sila import protobuf

from .data_type import DataType
from .list import List


@dataclasses.dataclass
class Element:
    """An element as part of the SiLA structure data type"""

    identifier: str = ""
    """
    Uniquely identifies the structure element within the scope of its structure data type. Uniqueness is checked without
    taking lower and upper case into account. Should be in pascal case.
    """

    display_name: str = ""
    """Human readable name of the structure element. Should be the identifier with spaces between separate words."""

    description: str = ""
    """Describes the use and purpose of the structure element."""

    data_type: DataType = dataclasses.field(default_factory=DataType)
    """The SiLA data type of the structure element."""


@dataclasses.dataclass
class Structure(DataType[dict]):
    """
    The SiLA structure type is a structure composed of one or more named elements with the same or different SiLA types.
    """

    Element: typing.ClassVar = Element

    elements: list[Structure.Element] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.__elements_by_identifier = {
            element.identifier: (index + 1, element) for index, element in enumerate(self.elements)
        }

    def encode(self, value: dict, field_number: int | None = None) -> bytes:
        stream = io.BytesIO()
        chunks = bytearray()

        for key, item in value.items():
            index, field = self.__elements_by_identifier[key]

            if field is None:
                continue

            data = field.data_type.encode(item, field_number=index)
            if not isinstance(field.data_type, List):
                chunks.append(protobuf.Tag(field_number=index, wire_type=protobuf.WireType.LEN).encode())
                t = io.BytesIO()
                protobuf.write_unsigned_varint(protobuf.uint(len(data)), t)
                chunks.extend(t.getvalue())
            chunks.extend(data)

        if field_number:
            protobuf.Tag(field_number=field_number or 1, wire_type=protobuf.WireType.LEN).write_to(stream)
            protobuf.write_unsigned_varint(protobuf.uint(len(chunks)), stream)
        stream.write(chunks)

        return stream.getvalue()

    def decode(self, data: bytes) -> dict:
        values: dict[str, dict] = {}
        stream = io.BytesIO(data)
        while True:
            try:
                cursor = stream.tell()
                tag = protobuf.Tag.read_from(stream)
            except EOFError:
                break
            try:
                field = self.elements[tag.field_number - 1]
            except IndexError:
                size = protobuf.read_unsigned_varint(stream)
                payload = stream.read(size)
            else:
                size = protobuf.read_unsigned_varint(stream)
                payload = stream.read(size)

                if isinstance(field.data_type, List):
                    values[field.identifier] = values.get(field.identifier, {"field": field, "payload": b""})
                    values[field.identifier]["payload"] += data[cursor : stream.tell()]
                else:
                    values[field.identifier] = {"field": field, "payload": payload}

        result = {}
        for element in self.elements:
            if isinstance(element.data_type, List) and element.identifier not in values:
                values[element.identifier] = {"field": element, "payload": b""}

            if element.identifier not in values:
                raise protobuf.MessageDecodeError(
                    field=element.identifier, msg=f"Missing field {element.identifier} in parameters."
                )

            try:
                value = (
                    values[element.identifier].get("field").data_type.decode(values[element.identifier].get("payload"))
                )
            except protobuf.MessageDecodeError as decode_error:
                raise protobuf.MessageDecodeError(field=element.identifier, msg=decode_error.msg) from decode_error
            else:
                result[element.identifier] = value

        return result
