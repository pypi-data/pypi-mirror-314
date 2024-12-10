import pytest

from totokenizers.openai import ChatMLMessage, OpenAITokenizer
from totokenizers.schemas import (
    ToolCall,
    ToolCallFunction,
    ToolCallMLMessage,
    ToolMLMessage,
)


@pytest.fixture(scope="function")
def tool_mlmessage():
    return [
        ToolMLMessage(
            content="The wether today is sunny.",
            name="tool response 1",
            role="tool",
        ),
        ToolMLMessage(
            content="Now, it is 10:00 AM.",
            name="tool response 2",
            role="tool",
        ),
    ]


@pytest.fixture(scope="function")
def tool_call_message():
    return [
        ToolCallMLMessage(
            content=None,
            tool_calls=[
                ToolCall(
                    type="function",
                    function=ToolCallFunction(
                        name="get_weather",
                        arguments="{'city': 'New York', 'date': '20/10/1021'}",
                    ),
                )
            ],
            role="assistant",
        ),
        ToolCallMLMessage(
            content=None,
            tool_calls=[
                ToolCall(
                    type="function",
                    function=ToolCallFunction(
                        name="get_weather",
                        arguments="{'city': 'New York'}",
                    ),
                )
            ],
            role="assistant",
        ),
    ]


@pytest.fixture(scope="function")
def tool_call_message_no_args():
    return [
        ToolCallMLMessage(
            content=None,
            tool_calls=[
                ToolCall(
                    type="function",
                    function=ToolCallFunction(name="time_now", arguments=""),
                )
            ],
            role="assistant",
        ),
    ]


@pytest.fixture(scope="module")
def chatml_messages():
    return [
        ChatMLMessage(
            content="You are a bot.",
            name="system",
            role="system",
        ),
        ChatMLMessage(
            content="hello bot",
            name="user",
            role="user",
        ),
        ChatMLMessage(
            content="I am Skynet.",
            name="skynet",
            role="assistant",
        ),
    ]


def test_gpp4_o(chatml_messages):
    tokenizer = OpenAITokenizer(model_name="gpt-4o-2024-05-13")

    count_tokens = tokenizer.count_chatml_tokens(chatml_messages)
    assert count_tokens == 34

    count_tokens = tokenizer.count_tokens("hello world")
    assert count_tokens == 2

    # TODO: count function call tokens


def test_gpt4_o_tools(tool_mlmessage):
    tokenizer = OpenAITokenizer(model_name="gpt-4o")

    count_tokens = tokenizer.count_tools_tokens(tool_mlmessage)
    assert count_tokens == 37


def test_gpt4_o_tool_call(tool_call_message, tool_call_message_no_args):
    tokenizer = OpenAITokenizer(model_name="gpt-4o")

    count_tokens = tokenizer.count_tools_tokens(tool_call_message)
    assert count_tokens == 57

    count_tokens = tokenizer.count_tools_tokens(tool_call_message_no_args)
    assert count_tokens == 22
