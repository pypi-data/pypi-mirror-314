import textwrap

from sila import metadata

from .serialize_data_type import serialize_data_type
from .serialize_defined_execution_error_list import serialize_defined_execution_error_list
from .serialize_description import serialize_description


def serialize_metadata(metadata_: metadata.Metadata) -> str:
    return (
        "<Metadata>\n"
        + textwrap.indent(
            f"<Identifier>{ metadata_.identifier }</Identifier>\n"
            + f"<DisplayName>{ metadata_.display_name }</DisplayName>\n"
            + serialize_description(metadata_.description)
            + "\n"
            + serialize_data_type(metadata_.message.elements[0].data_type)
            + "\n"
            + ((serialize_defined_execution_error_list(metadata_.errors) + "\n") if metadata_.errors else ""),
            "  ",
        )
        + "</Metadata>"
    )
