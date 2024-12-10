from typing import Literal, NotRequired, Sequence, TypedDict


class ChatTextContent(TypedDict):
    type: Literal["text"]
    text: str


class ImageURL(TypedDict):
    url: str
    detail: Literal["low", "high", "auto"]


class ChatImageContent(TypedDict):
    type: Literal["image_url"]
    image_url: ImageURL


class ChatMLMessage(TypedDict):
    content: str | list[ChatTextContent | ChatImageContent]
    name: NotRequired[str]
    role: Literal["user", "assistant", "system"]


class FunctionCall(TypedDict):
    name: str
    arguments: str


class FunctionCallChatMLMessage(TypedDict):
    content: None
    function_call: FunctionCall
    role: Literal["assistant"]


class FunctionChatMLMessage(TypedDict):
    content: str
    name: str
    role: Literal["function"]


class ToolCallFunction(TypedDict):
    arguments: str
    name: str


class ToolCall(TypedDict):
    type: Literal["function"]
    function: ToolCallFunction


class ToolCallMLMessage(TypedDict):
    content: None
    tool_calls: list[ToolCall]
    role: Literal["assistant"]


class ToolMLMessage(TypedDict):
    content: str
    name: str
    role: Literal["tool"]


Chat = Sequence[ChatMLMessage | FunctionCallChatMLMessage | FunctionChatMLMessage]
Tool = Sequence[ToolMLMessage | ToolCallMLMessage]
