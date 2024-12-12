import dataclasses
import enum

from sila import identifiers

from .constraint import Constraint


class Identifier(enum.Enum):
    FEATURE_IDENTIFIER = "FeatureIdentifier"
    COMMAND_IDENTIFIER = "CommandIdentifier"
    COMMAND_PARAMETER_IDENTIFIER = "CommandParameterIdentifier"
    COMMAND_RESPONSE_IDENTIFIER = "CommandResponseIdentifier"
    INTERMEDIATE_COMMAND_RESPONSE_IDENTIFIER = "IntermediateCommandResponseIdentifie"
    DEFINED_EXECUTION_ERROR_IDENTIFIER = "DefinedExecutionErrorIdentifier"
    PROPERTYI_DENTIFIER = "PropertyIdentifier"
    DATATYPE_IDENTIFIER = "DataTypeIdentifier"
    METADATA_IDENTIFIER = "MetadataIdentifier"


@dataclasses.dataclass
class FullyQualifiedIdentifier(Constraint[str]):
    """
    A Fully Qualified Identifier Constraint specifies the content of the SiLA String Type to be a Fully Qualified
    Identifier and indicates the type of the identifier. Note that this is comparable to a Pattern Constraint; that is,
    the content is not required to actually identify something, it just has to be a semantically correct Fully Qualified
    Identifier.
    """

    value: Identifier

    def __post_init__(self):
        value = Identifier(self.value)
        self.identifier: type[identifiers.FullyQualifiedIdentifier] = getattr(
            identifiers, f"FullyQualified{value.value}"
        )

    def validate(self, value: str) -> bool:
        if not isinstance(value, str):
            raise TypeError()
        if not self.identifier.parse(value):
            raise ValueError()

        return True
