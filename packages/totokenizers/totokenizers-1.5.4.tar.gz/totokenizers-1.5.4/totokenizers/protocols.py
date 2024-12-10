from typing import Any, Optional, Protocol, Union

from .schemas import (
    Chat,
    ChatMLMessage,
    FunctionCallChatMLMessage,
    FunctionChatMLMessage,
)


# TODO: type hint functions correctly
class Tokenizer(Protocol):
    model: str

    def encode(self, text: str) -> list[int]:
        ...

    def count_tokens(self, text: str) -> int:
        ...

    def count_chatml_tokens(
        self, messages: Chat, functions: Optional[list[dict[str, Any]]] = None
    ) -> int:
        ...

    def count_message_tokens(
        self,
        message: Union[ChatMLMessage, FunctionCallChatMLMessage, FunctionChatMLMessage],
    ) -> int:
        ...

    def count_functions_tokens(self, functions: Optional[list[dict[str, Any]]]) -> int:
        ...
