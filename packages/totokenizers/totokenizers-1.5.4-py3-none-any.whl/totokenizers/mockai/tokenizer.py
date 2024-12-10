import logging
from typing import Literal, Optional, Sequence, Mapping

from ..jsonschema_formatter import FunctionJSONSchema
from ..schemas import Chat, ChatMLMessage, FunctionCallChatMLMessage, FunctionChatMLMessage

logger = logging.getLogger("totokenizers")


class MockAITokenizer:

    def __init__(
        self,
        model_name: Literal["always-func", "always-chat"],
    ):
        self.model = model_name

    def encode(self, text: str) -> list[int]:
        return [1] * len(text)

    def count_tokens(self, text: str) -> int:
        return len(text)

    def count_chatml_tokens(
        self, messages: Chat, functions: Optional[Sequence[Mapping]] = None
    ) -> int:
        num_tokens = sum(map(self.count_message_tokens, messages))
        if functions:
            num_tokens += self.count_functions_tokens(functions)
        return num_tokens

    def count_message_tokens(self, message: ChatMLMessage | FunctionCallChatMLMessage | FunctionChatMLMessage) -> int:
        num_tokens = 0
        if message["role"] == "function":
            num_tokens += (
                self.count_tokens(message["content"])
                + self.count_tokens(message["name"])
                + self.count_tokens(message["role"])
            )
        elif "function_call" in message:
            num_tokens += (
                self.count_tokens(message["function_call"]["name"])
                + self.count_tokens(message["function_call"]["arguments"])  # TODO: what if there are no arguments?
                + self.count_tokens(message["role"])
            )
        else:
            num_tokens += (
                self.count_tokens(message["content"])
                + self.count_tokens(message["role"])
            )
            if "name" in message:
                num_tokens += self.count_tokens(message["name"])
        return num_tokens

    def count_functions_tokens(self, functions: list[dict]) -> int:
        num_tokens = len(self.encode(FunctionJSONSchema(functions).to_typescript()))
        return num_tokens
