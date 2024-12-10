import asyncio
import os
import textwrap
import uuid
from typing import Iterable, List, Literal, Optional, Tuple, Union, overload

import grpc
import grpc._grpcio_metadata
from google.protobuf.struct_pb2 import Struct
from grpc import aio
from vmxai_completion_client import (
    CompletionRequest as GrpcCompletionRequest,
)
from vmxai_completion_client import (
    CompletionResponse,
    CompletionServiceStub,
    GetResourceProviderCountRequest,
    GetResourceProviderCountResponse,
    RequestToolChoiceItem,
)
from vmxai_completion_client import (
    RequestMessage as GrpcRequestMessage,
)
from vmxai_completion_client import (
    RequestToolChoice as GrpcRequestToolChoice,
)
from vmxai_completion_client import (
    RequestToolFunction as GrpcRequestToolFunction,
)
from vmxai_completion_client import (
    RequestTools as GrpcRequestTools,
)

from vmxai.auth.api_key import VMXClientAPIKey
from vmxai.types import CompletionRequest, RequestTools


class VMXClient:
    def __init__(
        self,
        domain: str = os.getenv("VMX_DOMAIN", None),
        api_key: str = os.getenv("VMX_API_KEY", None),
        secure_channel: bool = os.getenv("VMX_SECURE_CHANNEL", "true").lower() == "true",
        workspace_id: Optional[str] = os.getenv("VMX_WORKSPACE_ID", None),
        environment_id: Optional[str] = os.getenv("VMX_ENVIRONMENT_ID", None),
    ):
        if not domain:
            raise AttributeError(
                textwrap.wrap("""
                'domain' must be provided.

                Or

                set the 'VMX_DOMAIN' environment variable.
                """)
            )

        self.domain = domain
        self.workspace_id = workspace_id
        self.environment_id = environment_id
        self.secure_channel = secure_channel

        if api_key:
            self.auth = VMXClientAPIKey(api_key)
        else:
            raise AttributeError(
                textwrap.wrap("""
                'api_key' must be provided.

                Or

                set the 'VMX_API_KEY' environment variable.

                Or

                set the 'VMX_OAUTH_CLIENT_ID' and 'VMX_OAUTH_CLIENT_SECRET' environment variables.
                """)
            )

        self.api_key = api_key

        self.completion_client = CompletionServiceStub(
            grpc.secure_channel(f"grpc.{self.domain}", grpc.ssl_channel_credentials())
            if self.secure_channel
            else grpc.insecure_channel(self.domain)
        )

    @overload
    def completion(
        self, *, request: CompletionRequest, multi_answer: Literal[True]
    ) -> Tuple[asyncio.Task[Iterable[CompletionResponse]], ...]: ...

    @overload
    def completion(
        self, *, request: CompletionRequest, multi_answer: Literal[True], answer_count: int
    ) -> Tuple[asyncio.Task[Iterable[CompletionResponse]], ...]: ...

    @overload
    def completion(self, *, request: CompletionRequest) -> Iterable[CompletionResponse]: ...

    @overload
    def completion(self, *, request: CompletionRequest, stream: Literal[True]) -> Iterable[CompletionResponse]: ...

    @overload
    def completion(
        self, *, request: CompletionRequest, stream: Literal[True], multi_answer: Literal[True]
    ) -> Tuple[asyncio.Task[Iterable[CompletionResponse]], ...]: ...

    @overload
    def completion(
        self, *, request: CompletionRequest, stream: Literal[True], multi_answer: Literal[True], answer_count: int
    ) -> Tuple[asyncio.Task[Iterable[CompletionResponse]], ...]: ...

    @overload
    def completion(self, *, request: CompletionRequest, stream: Literal[False]) -> CompletionResponse: ...

    @overload
    def completion(
        self, *, request: CompletionRequest, stream: Literal[False], multi_answer: Literal[True]
    ) -> Tuple[asyncio.Task[CompletionResponse], ...]: ...

    @overload
    def completion(
        self, *, request: CompletionRequest, stream: Literal[False], multi_answer: Literal[True], answer_count: int
    ) -> Tuple[asyncio.Task[CompletionResponse], ...]: ...

    def completion(
        self,
        *,
        request: CompletionRequest,
        stream: bool = True,
        multi_answer: bool = False,
        answer_count: Optional[int] = None,
    ) -> Union[
        Iterable[CompletionResponse],
        Tuple[asyncio.Task[Iterable[CompletionResponse]]],
        CompletionResponse,
        Tuple[asyncio.Task[CompletionResponse]],
    ]:
        metadata: list[tuple[str, str]] = []
        if "_X_AMZN_TRACE_ID" in os.environ:
            metadata.append(("x-amzn-trace-id", os.environ["_X_AMZN_TRACE_ID"]))

        metadata.append(("correlation-id", str(uuid.uuid4())))

        self.auth.inject_credentials(self, metadata)
        config = Struct()
        if request.config:
            config.update(request.config)

        grpc_request = dict(
            workspace_id=request.workspace_id or self.workspace_id,
            environment_id=request.environment_id or self.environment_id,
            resource=request.resource,
            config=config,
            stream=stream,
            tools=self._parse_tools(request.tools),
            tool_choice=self._parse_tool_choice(request.tool_choice),
            metadata=request.metadata or None,
            resource_config_overrides=request.resource_config_overrides or None,
            messages=[
                GrpcRequestMessage(
                    name=message.name,
                    role=message.role,
                    tool_call_id=message.tool_call_id,
                    tool_calls=message.tool_calls or [],
                    content=message.content,
                )
                for message in request.messages
            ],
        )

        if multi_answer and answer_count is None:
            provider_count_response: GetResourceProviderCountResponse = self.completion_client.getResourceProviderCount(
                GetResourceProviderCountRequest(
                    workspace_id=request.workspace_id or self.workspace_id,
                    environment_id=request.environment_id or self.environment_id,
                    resource=request.resource
                ), metadata=tuple(metadata)
            )

            answer_count = provider_count_response.count

        if stream:
            if not multi_answer:
                return self.completion_client.create(GrpcCompletionRequest(**grpc_request), metadata=tuple(metadata))

            return tuple(
                [
                    asyncio.create_task(self._call_multi_answer(index, grpc_request, metadata, stream))
                    for index in range(answer_count)
                ]
            )
        else:
            if not multi_answer:
                result = self.completion_client.create(GrpcCompletionRequest(**grpc_request), metadata=tuple(metadata))
                for response in result:
                    return response

            return tuple(
                [
                    asyncio.create_task(self._call_multi_answer(index, grpc_request, metadata, stream))
                    for index in range(answer_count)
                ]
            )

    async def _call_multi_answer(
        self,
        index: int,
        grpc_request: dict,
        metadata: List[Tuple[str, str]],
        stream: bool,
    ):
        primary = index == 0
        secondary_model_index = index - 1 if index > 0 else None

        if stream:
            return self.completion_client.create(
                GrpcCompletionRequest(primary=primary, secondary_model_index=secondary_model_index, **grpc_request),
                metadata=metadata,
            )
        else:
            async with (
                aio.secure_channel(f"grpc.{self.domain}", grpc.ssl_channel_credentials())
                if self.secure_channel
                else aio.insecure_channel(self.domain)
            ) as channel:
                result = CompletionServiceStub(channel).create(
                    GrpcCompletionRequest(primary=primary, secondary_model_index=secondary_model_index, **grpc_request),
                    metadata=metadata,
                )
                async for item in result:
                    return item

    def _parse_tools(self, tools: list[RequestTools]) -> list[GrpcRequestTools]:
        result: list[GrpcRequestTools] = []
        for tool in tools or []:
            grpc_function_params = Struct()
            grpc_function_params.update(tool.function.parameters)

            grpc_tool = GrpcRequestTools(
                type=tool.type,
                function=GrpcRequestToolFunction(
                    name=tool.function.name, description=tool.function.description, parameters=grpc_function_params
                ),
            )
            result.append(grpc_tool)

        return result

    def _parse_tool_choice(
        self, tool_choice: Union[Literal["auto", "none"], RequestToolChoiceItem]
    ) -> GrpcRequestToolChoice:
        if tool_choice == "auto":
            return GrpcRequestToolChoice(auto=True, none=False)
        elif tool_choice == "none":
            return GrpcRequestToolChoice(auto=False, none=True)
        else:
            return GrpcRequestToolChoice(auto=False, none=False, tool=tool_choice)
