from __future__ import annotations

import dataclasses

from .command import Command


@dataclasses.dataclass
class UnobservableCommand(Command):
    """
    Any Command for which observing the progress or status of the command execution on the SiLA Server is not possible
    or does not make sense.
    """

    observable: bool = dataclasses.field(init=False, repr=False, default=False)
