import dataclasses
import typing

from .constraint import Constraint

T = typing.TypeVar("T", str, bytes)


class ContentTypeParameter(typing.NamedTuple):
    attribute: str
    value: str


@dataclasses.dataclass
class ContentType(Constraint[T]):
    """
    A Content Type Constraint specifies the type of content of a binary or textual SiLA Data Type based on a RFC 2045
    ContentType.
    """

    Parameter: typing.ClassVar = ContentTypeParameter

    type: str

    subtype: str

    parameters: list[ContentTypeParameter] = dataclasses.field(default_factory=list)

    @property
    def media_type(self) -> str:
        return f"{self.type}/{self.subtype}" + "".join(
            [f"; {parameter.attribute}={parameter.value}" for parameter in self.parameters]
        )

    def validate(self, value: T) -> bool:
        if not isinstance(value, (str, bytes)):
            raise TypeError()

        return True
