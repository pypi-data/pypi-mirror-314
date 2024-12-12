import decimal
import textwrap

from sila import constraints

ctx = decimal.Context(prec=20)


def float_to_str(value: float) -> str:
    """Convert float to exact string representation, i.e. prevent scientific notation produced by float repr"""
    return format(ctx.create_decimal(repr(value)), "f")


def serialize_constraint(constraint: constraints.Constraint) -> str:
    if isinstance(constraint, constraints.Length):
        return f"<Length>{ constraint.value }</Length>"
    if isinstance(constraint, constraints.MinimalLength):
        return f"<MinimalLength>{ constraint.value }</MinimalLength>"
    if isinstance(constraint, constraints.MaximalLength):
        return f"<MaximalLength>{ constraint.value }</MaximalLength>"
    if isinstance(constraint, constraints.Set):
        return (
            "<Set>\n"
            + textwrap.indent("\n".join(f"<Value>{ value }</Value>" for value in constraint.value), "  ")
            + "\n</Set>"
        )
    if isinstance(constraint, constraints.Pattern):
        return f"<Pattern>{ constraint.value }</Pattern>"
    if isinstance(constraint, constraints.MaximalExclusive):
        return f"<MaximalExclusive>{ constraint.value }</MaximalExclusive>"
    if isinstance(constraint, constraints.MaximalInclusive):
        return f"<MaximalInclusive>{ constraint.value }</MaximalInclusive>"
    if isinstance(constraint, constraints.MinimalExclusive):
        return f"<MinimalExclusive>{ constraint.value }</MinimalExclusive>"
    if isinstance(constraint, constraints.MinimalInclusive):
        return f"<MinimalInclusive>{ constraint.value }</MinimalInclusive>"
    if isinstance(constraint, constraints.ElementCount):
        return f"<ElementCount>{ constraint.value }</ElementCount>"
    if isinstance(constraint, constraints.MinimalElementCount):
        return f"<MinimalElementCount>{ constraint.value }</MinimalElementCount>"
    if isinstance(constraint, constraints.MaximalElementCount):
        return f"<MaximalElementCount>{ constraint.value }</MaximalElementCount>"
    if isinstance(constraint, constraints.Unit):
        return (
            "<Unit>"
            + textwrap.indent(
                textwrap.dedent(
                    f"""
                    <Label>{ constraint.label }</Label>
                    <Factor>{ float_to_str(constraint.factor) }</Factor>
                    <Offset>{ float_to_str(constraint.offset) }</Offset>
                    """
                )
                + "\n".join(
                    "<UnitComponent>"
                    + textwrap.indent(
                        textwrap.dedent(
                            f"""
                            <SIUnit>{ component.unit.value }</SIUnit>
                            <Exponent>{ component.exponent }</Exponent>
                            """
                        ),
                        "  ",
                    )
                    + "</UnitComponent>"
                    for component in constraint.components
                ),
                "  ",
            )
            + "\n</Unit>"
        )
    if isinstance(constraint, constraints.ContentType):
        return (
            "<ContentType>"
            + textwrap.indent(
                textwrap.dedent(
                    f"""
                    <Type>{ constraint.type }</Type>
                    <Subtype>{ constraint.subtype }</Subtype>
                    """
                )
                + (
                    (
                        "<Parameters>\n"
                        + textwrap.indent(
                            "\n".join(
                                "<Parameter>"
                                + textwrap.indent(
                                    textwrap.dedent(
                                        f"""
                                <Attribute>{ parameter.attribute }</Attribute>
                                <Value>{ parameter.value }</Value>
                                """
                                    ),
                                    "  ",
                                )
                                + "</Parameter>"
                                for parameter in constraint.parameters
                            ),
                            "  ",
                        )
                        + "\n</Parameters>"
                    )
                    if len(constraint.parameters)
                    else ""
                ),
                "  ",
            )
            + "\n</ContentType>"
        )
    if isinstance(constraint, constraints.FullyQualifiedIdentifier):
        return f"<FullyQualifiedIdentifier>{ constraint.value.value }</FullyQualifiedIdentifier>"
    if isinstance(constraint, constraints.Schema):
        return (
            "<Schema>\n"
            + textwrap.indent(
                f"<Type>{ constraint.type.value }</Type>\n"
                + (f"<Url>{ constraint.url }</Url>\n" if constraint.url else "")
                + (f"<Inline>\n{ textwrap.indent(constraint.inline, '  ') }\n</Inline>\n" if constraint.inline else ""),
                "  ",
            )
            + "</Schema>"
        )
    if isinstance(constraint, constraints.AllowedTypes):
        from .serialize_data_type import serialize_data_type

        return (
            "<AllowedTypes>\n"
            + textwrap.indent("\n".join(serialize_data_type(value) for value in constraint.value), "  ")
            + "\n</AllowedTypes>"
        )
    return ""
