from __future__ import annotations

import dataclasses
import typing

from sila import protobuf


@dataclasses.dataclass
class CommandExecutionUUID(protobuf.BaseMessage):
    """
    A Command Execution UUID is the UUID of a Command execution. It is unique within one instance of a SiLA Server and
    its lifetime (Lifetime of a SiLA Server).
    """

    value: typing.Annotated[str, protobuf.Field(1)] = ""
    """The UUID of a Command execution."""
