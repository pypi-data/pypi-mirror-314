from __future__ import annotations

import dataclasses
import typing

from sila import protobuf

from .sila_exception import SiLAException


@dataclasses.dataclass
class UndefinedExecutionError(SiLAException, protobuf.BaseMessage):
    """
    Any Execution Error which is not a Defined Execution Error is an Undefined Execution Error. These types of errors
    are implementation dependent and occur unexpectedly and cannot be foreseen by the Feature Designer and hence cannot
    be specified as part of the Feature. The Undefined Execution Error MUST include human readable information in the
    American English language about the error and SHOULD provide proposals for how to resolve the error.
    """

    message: typing.Annotated[str, protobuf.Field(1)]
    """
    Human readable information in the American English language about the error and proposals for how to resolve the
    error.
    """
