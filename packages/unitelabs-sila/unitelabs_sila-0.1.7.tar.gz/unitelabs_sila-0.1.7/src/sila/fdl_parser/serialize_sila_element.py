import textwrap
import typing

from sila import data_types

from .serialize_data_type import serialize_data_type
from .serialize_description import serialize_description


class SiLAElement(typing.Protocol):
    identifier: str
    display_name: str
    description: str
    data_type: data_types.DataType


def serialize_sila_element(element: SiLAElement, tag: str) -> str:
    return (
        f"<{tag}>\n"
        + textwrap.indent(
            f"<Identifier>{ element.identifier }</Identifier>\n"
            + f"<DisplayName>{ element.display_name }</DisplayName>\n"
            + serialize_description(element.description)
            + "\n"
            + serialize_data_type(element.data_type),
            "  ",
        )
        + f"\n</{tag}>"
    )
