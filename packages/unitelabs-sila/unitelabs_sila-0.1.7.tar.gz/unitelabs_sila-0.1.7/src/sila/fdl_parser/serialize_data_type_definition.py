import textwrap

from sila import data_types

from .serialize_data_type import serialize_data_type
from .serialize_description import serialize_description


def serialize_data_type_definition(data_type_definition: data_types.DataTypeDefinition) -> str:
    return (
        "<DataTypeDefinition>\n"
        + textwrap.indent(
            f"<Identifier>{ data_type_definition.identifier }</Identifier>\n"
            + f"<DisplayName>{ data_type_definition.display_name }</DisplayName>\n"
            + serialize_description(data_type_definition.description)
            + "\n"
            + serialize_data_type(data_type_definition.message.elements[0].data_type)
            + "\n",
            "  ",
        )
        + "</DataTypeDefinition>"
    )
