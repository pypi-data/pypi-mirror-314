import textwrap

from sila import errors

from .serialize_description import serialize_description


def serialize_defined_execution_error(defined_execution_error: errors.DefinedExecutionError):
    return (
        "<DefinedExecutionError>\n"
        + textwrap.indent(
            f"<Identifier>{ defined_execution_error.identifier }</Identifier>\n"
            + f"<DisplayName>{ defined_execution_error.display_name }</DisplayName>\n"
            + serialize_description(defined_execution_error.description),
            "  ",
        )
        + "\n</DefinedExecutionError>"
    )
