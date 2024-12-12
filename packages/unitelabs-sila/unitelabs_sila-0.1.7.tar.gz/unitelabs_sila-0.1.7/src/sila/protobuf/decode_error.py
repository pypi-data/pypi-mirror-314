import dataclasses


@dataclasses.dataclass
class MessageDecodeError(ValueError):
    """Subclass of ValueError with the following additional attributes:"""

    msg: str = ""
    """The unformatted error message."""

    doc: bytes = b""
    """The byte message being parsed."""

    num: int = 0
    """The field number of the field where parsing failed."""

    field: str = ""
    """The field name of the field where parsing failed."""
