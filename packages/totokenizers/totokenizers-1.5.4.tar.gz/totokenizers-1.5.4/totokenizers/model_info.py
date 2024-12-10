from dataclasses import dataclass, field
from typing import Literal


@dataclass
class ModelInfo:
    """
    Struct for model information.

    Would be lovely to eventually get this directly from APIs.
    But it needs to be scraped from websites for now.
    """

    name: str
    max_tokens: int
    prompt_token_cost: float
    cutoff: str


@dataclass
class CompletionModelInfo(ModelInfo):
    """Struct for generic completion model information."""

    completion_token_cost: float


@dataclass
class ChatModelInfo(CompletionModelInfo):
    """Struct for chat model information."""

    max_output_tokens: int
    feature_flags: list[Literal["functions", "tools", "json", "vision", "voice"]] = field(
        default_factory=list
    )
    deprecated: bool = False


@dataclass
class TextModelInfo(CompletionModelInfo):
    """Struct for text completion model information."""


@dataclass
class EmbeddingModelInfo(ModelInfo):
    """Struct for embedding model information."""

    default_dim: int
    supported_dim: list[int]
