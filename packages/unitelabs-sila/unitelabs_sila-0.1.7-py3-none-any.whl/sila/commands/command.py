from __future__ import annotations

import dataclasses

from sila import core, data_types, identifiers


@dataclasses.dataclass
class Command(core.Handler):
    """A command models an action that will be performed on a SiLA server."""

    parameters: data_types.Structure = dataclasses.field(repr=False, default_factory=data_types.Structure)
    """The parameters of the command."""

    responses: data_types.Structure = dataclasses.field(repr=False, default_factory=data_types.Structure)
    """The responses of the command containing the result."""

    @property
    def fully_qualified_identifier(self) -> identifiers.FullyQualifiedCommandIdentifier:
        if self.feature is None:
            raise UnboundLocalError()

        feature_identifier = self.feature.fully_qualified_identifier
        return identifiers.FullyQualifiedCommandIdentifier(
            **dataclasses.asdict(feature_identifier), command=self.identifier
        )
