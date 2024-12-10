from dataclasses import dataclass, field
from typing import Literal, Optional, Union

from vmxai_completion_client import RequestMessageToolCall, RequestToolChoiceItem


@dataclass
class RequestToolFunction:
    name: str
    description: str
    parameters: dict


@dataclass
class RequestTools:
    type: Literal["function"]
    function: RequestToolFunction


@dataclass
class RequestMessage:
    role: Literal["system", "user", "assistant", "tool"]
    name: Optional[str] = field(default=None)
    content: Optional[str] = field(default=None)
    tool_call_id: Optional[str] = field(default=None)
    tool_calls: Optional[list[RequestMessageToolCall]] = field(default_factory=list)


@dataclass
class CompletionRequest:
    resource: str
    workspace_id: Optional[str] = None
    environment_id: Optional[str] = None
    tools: Optional[list[RequestTools]] = field(default_factory=list)
    tool_choice: Optional[Union[Literal["auto", "none"], RequestToolChoiceItem]] = "auto"
    config: Optional[dict] = field(default_factory=dict)
    messages: list[RequestMessage] = field(default_factory=list)
    resource_config_overrides: Optional[dict] = field(default_factory=dict)
    metadata: Optional[dict] = field(default_factory=dict)
