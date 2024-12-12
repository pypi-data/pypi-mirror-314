from __future__ import annotations

import dataclasses
import typing

from sila import identifiers, validators

if typing.TYPE_CHECKING:
    from sila import commands, data_types, metadata, properties


@dataclasses.dataclass
class Feature:
    """
    Each feature describes a specific behavior of a SiLA server (e.g. the ability to measure a spectrum, to register a
    sample in a LIMS, control heating, etc.). Features are implemented by a SiLA server and used by a SiLA client. The
    SiLA service feature must be implemented by each SiLA server. The SiLA service feature offers basic information
    about the SiLA server and about all other features the SiLA server implements.
    """

    locale: str = dataclasses.field(repr=False, default="en-us")
    sila2_version: str = dataclasses.field(repr=False, default="1.1")
    version: str = dataclasses.field(repr=False, default="1.0")
    maturity_level: str = dataclasses.field(repr=False, default="Draft")
    originator: str = dataclasses.field(repr=False, default="ch.unitelabs")
    category: str = dataclasses.field(repr=False, default="core")

    identifier: validators.Identifier = validators.Identifier()
    """
    A feature identifier is the identifier of a feature. Each feature must have a feature identifier. All features
    sharing the scope of the same originator and category must have unique feature identifiers. Uniqueness must be
    checked without taking lower and upper case into account.
    """

    display_name: validators.DisplayName = validators.DisplayName()
    """Human readable name of the SiLA feature."""

    description: str = dataclasses.field(repr=False, default="")
    """
    A feature description is the description of a feature. A feature description must describe the behaviors /
    capabilities the feature models in human readable form and with as many details as possible.
    """

    commands: dict[identifiers.FullyQualifiedCommandIdentifier, commands.Command] = dataclasses.field(
        init=False, repr=False, default_factory=dict
    )

    properties: dict[identifiers.FullyQualifiedPropertyIdentifier, properties.Property] = dataclasses.field(
        init=False, repr=False, default_factory=dict
    )

    metadata: dict[identifiers.FullyQualifiedMetadataIdentifier, metadata.Metadata] = dataclasses.field(
        init=False, repr=False, default_factory=dict
    )

    data_type_definitions: dict[identifiers.FullyQualifiedCustomDataTypeIdentifier, data_types.DataTypeDefinition] = (
        dataclasses.field(init=False, repr=False, default_factory=dict)
    )

    @property
    def fully_qualified_identifier(self) -> identifiers.FullyQualifiedFeatureIdentifier:
        return identifiers.FullyQualifiedFeatureIdentifier(
            self.originator, self.category, self.identifier, self.version.rpartition(".")[0]
        )

    def get_command(self, identifier: str) -> commands.Command:
        """Get a command based on its fully qualified identifier."""
        try:
            return self.commands[identifiers.FullyQualifiedCommandIdentifier.parse(identifier)]
        except (AttributeError, KeyError, ValueError):
            raise ValueError(f"Unknown command with identifier {identifier}") from None

    def get_property(self, identifier: str) -> properties.Property:
        """Get a property based on its fully qualified identifier."""
        try:
            return self.properties[identifiers.FullyQualifiedPropertyIdentifier.parse(identifier)]
        except (AttributeError, KeyError, ValueError):
            raise ValueError(f"Unknown property with identifier {identifier}") from None

    def __eq__(self, other) -> bool:
        return (
            hasattr(other, "fully_qualified_identifier")
            and getattr(other, "fully_qualified_identifier") == self.fully_qualified_identifier
        )
