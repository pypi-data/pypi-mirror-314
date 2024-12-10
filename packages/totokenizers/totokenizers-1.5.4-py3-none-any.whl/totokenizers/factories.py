from typing import Literal, overload

from .anthropic import ANTHROPIC_MODELS, AnthropicTokenizer
from .errors import BadFormatForModelTag, ModelNotFound, ModelProviderNotFound
from .mockai.info import MODELS as MOCKAI_MODELS
from .mockai.tokenizer import MockAITokenizer
from .openai import OpenAITokenizer
from .openai_info import OPEN_AI_MODELS

TokenizerType = OpenAITokenizer | AnthropicTokenizer | MockAITokenizer


class Totokenizer:

    @classmethod
    def from_model(cls, model: str) -> TokenizerType:
        try:
            provider, model_name = model.split("/", 1)
        except (ValueError, TypeError):
            raise BadFormatForModelTag(model)
        return cls.from_provider(provider, model_name)

    @overload
    @classmethod
    def from_provider(
        cls, provider: Literal["openai"], model: str
    ) -> OpenAITokenizer: ...
    @overload
    @classmethod
    def from_provider(
        cls, provider: Literal["anthropic"], model: str
    ) -> AnthropicTokenizer: ...
    @overload
    @classmethod
    def from_provider(
        cls, provider: Literal["mockai"], model: str
    ) -> MockAITokenizer: ...

    @classmethod
    def from_provider(cls, provider: str, model: str) -> TokenizerType:
        # use pattern matching
        match provider:
            case "anthropic":
                return AnthropicTokenizer(model)
            case "openai":
                return OpenAITokenizer(model)
            case "mockai":
                return MockAITokenizer(model)
            case _:
                raise ModelProviderNotFound(provider)

    def encode(self, text: str) -> list[int]:
        raise NotImplementedError

    def count_tokens(self, text: str) -> int:
        raise NotImplementedError


class TotoModelInfo:

    @classmethod
    def from_model(cls, model: str):
        try:
            provider, model_name = model.split("/", 1)
        except ValueError:
            raise BadFormatForModelTag(model)
        if provider == "anthropic":
            if model_name not in ANTHROPIC_MODELS:
                raise ModelNotFound(model_name)
            return ANTHROPIC_MODELS[model_name]
        if provider == "openai":
            if model_name not in OPEN_AI_MODELS:
                raise ModelNotFound(model_name)
            return OPEN_AI_MODELS[model_name]
        if provider == "mockai":
            if model_name not in MOCKAI_MODELS:
                raise ModelNotFound(model_name)
            return MOCKAI_MODELS[model_name]
        raise ModelProviderNotFound(provider)
