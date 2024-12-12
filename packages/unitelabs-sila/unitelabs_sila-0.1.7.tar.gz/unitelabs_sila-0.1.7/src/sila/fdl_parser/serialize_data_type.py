import textwrap

from sila import constraints, data_types

from .serialize_constraint import serialize_constraint
from .serialize_description import serialize_description


def serialize_data_type(data_type: data_types.DataType) -> str:
    if isinstance(data_type, data_types.List):
        return (
            "<DataType>\n"
            + textwrap.indent(
                "<List>\n" + textwrap.indent(serialize_data_type(data_type.data_type), "  ") + "\n</List>",
                "  ",
            )
            + "\n</DataType>"
        )
    if isinstance(data_type, data_types.Constrained):
        return (
            "<DataType>\n"
            + textwrap.indent(
                "<Constrained>\n"
                + textwrap.indent(
                    serialize_data_type(data_type.data_type)
                    + "\n<Constraints>\n"
                    + textwrap.indent(
                        "\n".join(serialize_constraint(constraint) for constraint in data_type.constraints), "  "
                    )
                    + "\n</Constraints>",
                    "  ",
                )
                + "\n</Constrained>",
                "  ",
            )
            + "\n</DataType>"
        )
    if isinstance(data_type, data_types.DataTypeDefinition):
        return (
            "<DataType>\n"
            + textwrap.indent(
                f"<DataTypeIdentifier>{ data_type.identifier }</DataTypeIdentifier>",
                "  ",
            )
            + "\n</DataType>"
        )
    if isinstance(data_type, data_types.Structure):
        return (
            "<DataType>\n"
            + textwrap.indent(
                "<Structure>\n"
                + textwrap.indent(
                    "".join(
                        "<Element>\n"
                        + textwrap.indent(
                            f"<Identifier>{ element.identifier }</Identifier>\n"
                            + f"<DisplayName>{ element.display_name }</DisplayName>\n"
                            + serialize_description(element.description)
                            + "\n"
                            + serialize_data_type(element.data_type),
                            "  ",
                        )
                        + "\n</Element>\n"
                        for element in data_type.elements
                    ),
                    "  ",
                )
                + "</Structure>",
                "  ",
            )
            + "\n</DataType>"
        )
    if isinstance(data_type, data_types.Void):
        return (
            "<DataType>\n"
            + textwrap.indent(
                "<Constrained>\n"
                + textwrap.indent(
                    serialize_data_type(data_types.String())
                    + "\n<Constraints>\n"
                    + textwrap.indent(serialize_constraint(constraints.Length(value=0)), "  ")
                    + "\n</Constraints>",
                    "  ",
                )
                + "\n</Constrained>",
                "  ",
            )
            + "\n</DataType>"
        )

    return f"<DataType>\n  <Basic>{data_type.__class__.__name__}</Basic>\n</DataType>"
