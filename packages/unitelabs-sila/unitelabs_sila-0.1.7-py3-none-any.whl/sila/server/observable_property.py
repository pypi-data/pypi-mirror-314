from __future__ import annotations

import base64
import dataclasses
import inspect
from collections.abc import AsyncIterator

import grpc
import grpc.aio

from sila import errors, properties

from .handler import Handler


@dataclasses.dataclass
class ObservableProperty(properties.ObservableProperty, Handler):
    async def execute(self, metadata: dict) -> AsyncIterator[bytes]:
        if self.feature is None or self.feature.server is None:
            raise RuntimeError("Cannot execute unbound property.")

        try:
            for feature in self.feature.server.features.values():
                for interceptor in feature.metadata.values():
                    interceptor.intercept(self, metadata)
        except errors.DefinedExecutionError as error:
            raise errors.FrameworkError(
                error_type=errors.FrameworkError.Type.INVALID_METADATA, message=error.description
            )
        try:
            responses = self.function()

            if inspect.isasyncgen(responses):
                async for response in responses:
                    yield self.message.encode({self.identifier: response})

            if inspect.isgenerator(responses):
                for response in responses:
                    yield self.message.encode({self.identifier: response})

        except errors.DefinedExecutionError as error:
            error.feature = self.feature
            raise error
        except errors.SiLAException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-exception-caught
            raise errors.UndefinedExecutionError(str(error))

    async def rpc_method_handler(
        self,
        message: bytes,  # pylint: disable=unused-argument
        context: grpc.aio.ServicerContext,
    ) -> AsyncIterator[bytes]:
        """
        The implementation of the RPC handler that accepts one request and returns either one response or an iterator of
        response values.

        Parameters:
            message: The binary representation of the request message.
            context: A context object of the RPC call.

        Returns:
            The binary representation of the response message.
        """
        try:
            metadata = dict(context.invocation_metadata() or {})
            async for value in self.execute(metadata):
                yield value
        except errors.SiLAException as error:
            exception = errors.SiLAError.from_exception(error)
            details = base64.standard_b64encode(bytes(exception)).decode("ascii")
            await context.abort(code=grpc.StatusCode.ABORTED, details=details)

    def add_to_feature(self, feature):
        super().add_to_feature(feature=feature)
        feature.properties[self.fully_qualified_identifier] = self
        feature.handlers[f"Subscribe_{self.identifier}"] = grpc.unary_stream_rpc_method_handler(self.rpc_method_handler)
