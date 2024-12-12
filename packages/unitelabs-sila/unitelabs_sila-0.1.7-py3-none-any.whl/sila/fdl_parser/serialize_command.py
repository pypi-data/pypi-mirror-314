import textwrap

from sila import commands

from .serialize_defined_execution_error_list import serialize_defined_execution_error_list
from .serialize_description import serialize_description
from .serialize_sila_element import serialize_sila_element


def serialize_command(command: commands.Command) -> str:
    return (
        "<Command>\n"
        + textwrap.indent(
            f"<Identifier>{ command.identifier }</Identifier>\n"
            + f"<DisplayName>{ command.display_name }</DisplayName>\n"
            + serialize_description(command.description)
            + "\n"
            + f"<Observable>{ 'Yes' if command.observable else 'No' }</Observable>\n"
            + "\n".join(serialize_sila_element(parameter, tag="Parameter") for parameter in command.parameters.elements)
            + ("\n" if command.parameters.elements else "")
            + "\n".join(serialize_sila_element(response, tag="Response") for response in command.responses.elements)
            + ("\n" if command.responses.elements else "")
            + (
                (
                    "\n".join(
                        serialize_sila_element(response, tag="IntermediateResponse")
                        for response in command.intermediate_responses.elements
                    )
                    + "\n"
                    if command.intermediate_responses.elements
                    else ""
                )
                if isinstance(command, commands.ObservableCommand)
                else ""
            )
            + ((serialize_defined_execution_error_list(command.errors) + "\n") if command.errors else ""),
            "  ",
        )
        + "</Command>"
    )
