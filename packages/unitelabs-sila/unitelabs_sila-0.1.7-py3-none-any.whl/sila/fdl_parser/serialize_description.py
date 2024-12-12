import textwrap


def serialize_description(description: str) -> str:
    if len(description) > 86:
        return f"<Description>\n{ textwrap.indent(description, '  ') }\n</Description>"
    return f"<Description>{ description }</Description>"
