import textwrap

from sila import properties

from .serialize_data_type import serialize_data_type
from .serialize_defined_execution_error_list import serialize_defined_execution_error_list
from .serialize_description import serialize_description


def serialize_property(property_: properties.Property) -> str:
    return (
        "<Property>\n"
        + textwrap.indent(
            f"<Identifier>{ property_.identifier }</Identifier>\n"
            + f"<DisplayName>{ property_.display_name }</DisplayName>\n"
            + serialize_description(property_.description)
            + "\n"
            + f"<Observable>{ 'Yes' if property_.observable else 'No' }</Observable>\n"
            + serialize_data_type(property_.message.elements[0].data_type)
            + "\n"
            + ((serialize_defined_execution_error_list(property_.errors) + "\n") if property_.errors else ""),
            "  ",
        )
        + "</Property>"
    )
