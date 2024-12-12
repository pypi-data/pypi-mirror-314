import dataclasses
import enum
import typing

from .constraint import Constraint

T = typing.TypeVar("T", bound=typing.Union[str, bytes])


class SchemaType(enum.Enum):
    XML = "Xml"
    JSON = "Json"


@dataclasses.dataclass
class Schema(Constraint[T]):
    """
    A Schema Constraint specifies the type of content of a binary or textual SiLA Data Type based on a schema, see
    Schema Constraint for a definition of the allowed Constraint Values.
    """

    Type: typing.ClassVar = SchemaType

    type: SchemaType

    url: typing.Optional[str] = None

    inline: typing.Optional[str] = None

    def validate(self, value: T) -> bool:
        return True
