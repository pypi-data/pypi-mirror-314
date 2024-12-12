import textwrap

from sila import errors


def serialize_defined_execution_error_list(defined_execution_errors: list[errors.DefinedExecutionError]) -> str:
    return (
        "<DefinedExecutionErrors>\n"
        + textwrap.indent(
            "\n".join(f"<Identifier>{ error.identifier }</Identifier>" for error in defined_execution_errors),
            "  ",
        )
        + "\n</DefinedExecutionErrors>"
    )
