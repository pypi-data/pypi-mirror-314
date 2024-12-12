from __future__ import annotations

import dataclasses

from sila import data_types

from .command import Command


@dataclasses.dataclass
class ObservableCommand(Command):
    """
    Any Command for which observing the progress or status of the command execution on the SiLA Server is possible and
    makes sense.
    """

    observable: bool = dataclasses.field(init=False, repr=False, default=True)

    intermediate_responses: data_types.Structure = dataclasses.field(repr=False, default_factory=data_types.Structure)
    """An intermediate response of the command execution containing the current result."""
