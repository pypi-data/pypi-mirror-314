import pytest

from totokenizers.factories import Totokenizer
from totokenizers.anthropic import AnthropicTokenizer


@pytest.fixture(scope="module")
def model_name():
    return "claude-2.1"


@pytest.fixture(scope="module")
def model_tag(model_name: str):
    return f"anthropic/{model_name}"


def test_factory(model_tag: str):
    tokenizer = Totokenizer.from_model(model_tag)
    assert isinstance(tokenizer, AnthropicTokenizer)


def test_count_tokens(model_tag: str):
    tokenizer = Totokenizer.from_model(model_tag)
    message = "hello world"
    assert tokenizer.count_tokens(message) == 2
