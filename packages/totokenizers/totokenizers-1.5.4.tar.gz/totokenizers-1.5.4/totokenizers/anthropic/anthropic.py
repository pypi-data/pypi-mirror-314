from pathlib import Path
from typing import Literal, Sequence

from tokenizers import (
    Encoding,
    Tokenizer as HFTokenizer,
)

from ..schemas import ChatMLMessage


class AnthropicTokenizer:
    """
    Tokenizer for the Anthropic AI models (Messages API).

    Args:
        model_name (str): The name of the model to use.

    Anthropic provides its tokenizer within their Python SDK:
    https://github.com/anthropics/anthropic-sdk-python/blob/main/src/anthropic/tokenizer.json

    The tokenizer is based on HuggingFace's `tokenizers` package:
    https://github.com/huggingface/tokenizers
    """
    def __init__(
        self,
        model_name: Literal[
            "claude-2.1",
            "claude-instant-1.2",
        ],
    ):
        self.tokenizer_path = Path(__file__).parent / "tokenizer.json"
        self.encoder: HFTokenizer = HFTokenizer.from_file(str(self.tokenizer_path))
        self.model_name = model_name

    def encode(self, text: str) -> list[int]:
        encoded: Encoding = self.encoder.encode(text)
        return encoded.ids

    def count_tokens(self, text: str) -> int:
        """Counts the number of tokens in a given text."""
        return len(self.encode(text))

    def _message_to_string(self, message: ChatMLMessage) -> str:
        if message["role"].lower() == "system":
            return message["content"]
        return f"\n\n{message['role'].lower()}: {message['content']}"

    def count_chatml_message_tokens(self, message: ChatMLMessage) -> int:
        raw_message = self._message_to_string(message)
        return self.count_tokens(raw_message)

    def count_chatml_tokens(self, messages: Sequence[ChatMLMessage]) -> int:
        num_tokens = sum(map(self.count_chatml_message_tokens, messages))
        return num_tokens

    def count_chatml_prompt_tokens(self, messages: Sequence[ChatMLMessage]) -> int:
        """Returns a count that matches the "prompt tokens" in the logs."""
        num_tokens = self.count_chatml_tokens(messages)
        # A message completion prompt always ends in "\n\nassistant:"
        if messages[-1]["role"].lower() != "assistant":
            num_tokens += self.count_tokens("\n\nassistant:")
        # Also, we are underestimating by 1 token according to the API logs
        num_tokens += 1
        return num_tokens

    def count_completion_tokens(self, text: str) -> int:
        """Returns a count that matches the "completion tokens" in the logs."""
        # A completion response always starts with "\n\nassistant:"
        num_tokens = self.count_tokens("\n\nassistant:")
        num_tokens += self.count_tokens(text)
        return num_tokens
