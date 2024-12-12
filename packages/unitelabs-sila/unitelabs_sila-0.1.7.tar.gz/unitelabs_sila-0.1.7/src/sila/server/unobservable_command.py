from __future__ import annotations

import base64
import dataclasses
import inspect

import grpc
import grpc.aio

from sila import commands, errors, protobuf

from .handler import Handler


@dataclasses.dataclass
class UnobservableCommand(commands.UnobservableCommand, Handler):
    async def execute(self, message: bytes = b"", metadata: dict | None = None) -> bytes:
        if self.feature is None or self.feature.server is None:
            raise RuntimeError("Cannot execute unbound command.")

        try:
            for feature in self.feature.server.features.values():
                for interceptor in feature.metadata.values():
                    interceptor.intercept(self, metadata or {})
        except errors.DefinedExecutionError as error:
            raise errors.FrameworkError(
                error_type=errors.FrameworkError.Type.INVALID_METADATA, message=error.description
            )
        try:
            parameters = self.parameters.decode(message)
        except protobuf.MessageDecodeError as error:
            raise errors.ValidationError(
                parameter=f"{self.fully_qualified_identifier}/Parameter/{error.field}", message=error.msg
            )
        try:
            responses = self.function(**parameters)

            if inspect.isawaitable(responses):
                responses = await responses

            return self.responses.encode(responses or {})
        except errors.DefinedExecutionError as error:
            error.feature = self.feature
            raise error
        except errors.SiLAException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-exception-caught
            raise errors.UndefinedExecutionError(str(error))

    async def rpc_method_handler(self, message: bytes, context: grpc.aio.ServicerContext) -> bytes:
        try:
            metadata = dict(context.invocation_metadata() or {})
            return await self.execute(message, metadata)
        except errors.SiLAException as error:
            exception = errors.SiLAError.from_exception(error)
            details = base64.standard_b64encode(bytes(exception)).decode("ascii")
            await context.abort(code=grpc.StatusCode.ABORTED, details=details)

    def add_to_feature(self, feature):
        super().add_to_feature(feature=feature)
        feature.commands[self.fully_qualified_identifier] = self
        feature.handlers[self.identifier] = grpc.unary_unary_rpc_method_handler(self.rpc_method_handler)
