import pytest

from totokenizers.factories import Totokenizer
from totokenizers.schemas import ChatMLMessage, Chat
from totokenizers.openai import OpenAITokenizer
from totokenizers.jsonschema_formatter import FunctionJSONSchema


@pytest.fixture(scope="module")
def model_name():
    return "gpt-3.5-turbo-0613"


@pytest.fixture(scope="module")
def model_tag(model_name: str):
    return f"openai/{model_name}"


def test_factory(model_tag: str):
    tokenizer = Totokenizer.from_model(model_tag)
    assert isinstance(tokenizer, OpenAITokenizer)


def test_simple_user_message(model_tag: str):
    tokenizer = Totokenizer.from_model(model_tag)
    user_message_example: ChatMLMessage = {
        "content": "Call the example function.",
        "role": "user",
    }
    assert tokenizer.count_message_tokens(user_message_example) == 9


def test_simple_chat(model_tag: str):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [
        {"content": "Good bot.", "role": "system"},
        {"content": "Hello.", "role": "user"},
    ]
    assert tokenizer.count_chatml_tokens(simple_chat) == 16


def test_functions_chat(model_tag: str, example_function_jsonschema: dict):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [
        {"content": "Good bot.", "role": "system"},
        {"content": "Hello.", "role": "user"},
    ]
    functions = [example_function_jsonschema]
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 70


def test_functions_chat_systemless(model_tag: str, example_function_jsonschema: dict):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [{"content": "Hello.", "role": "user"}]
    functions = [example_function_jsonschema]
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 67


def test_2_functions_chat(
    model_tag: str,
    example_function_jsonschema: dict,
    example_function2_jsonschema: dict,
):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [
        {"content": "Good bot.", "role": "system"},
        {"content": "Hello.", "role": "user"},
    ]
    functions = [example_function_jsonschema, example_function2_jsonschema]
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 134


def test_2_functions_chat_systemless(
    model_tag: str,
    example_function_jsonschema: dict,
    example_function2_jsonschema: dict,
):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [{"content": "Hello.", "role": "user"}]
    functions = [example_function_jsonschema, example_function2_jsonschema]
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 131


def test_function_call_chat(
    model_tag: str,
    example_function_jsonschema: dict,
):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [
        {"content": "Debug bot.", "role": "system"},
        {"content": "Call the example function.", "role": "user"},
        {
            "content": None,
            "function_call": {
            "name": "exampleFunction",
            "arguments": "{\n  \"param1\": \"Hello\",\n  \"param2\": 123\n}"
            },
            "role": "assistant",
        },
        {"content": "example return: ('Hello', 42)", "name": "exampleFunction", "role": "function"},
    ]
    functions = [example_function_jsonschema]
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 114


def test_function_call_chat_systemless(
    model_tag: str,
    example_function_jsonschema: dict,
):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [
        {"content": "Call the example function.", "role": "user"},
        {
            "content": None,
            "function_call": {
            "name": "exampleFunction",
            "arguments": "{\n  \"param1\": \"Hello\",\n  \"param2\": 123\n}"
            },
            "role": "assistant",
        },
        {"content": "example return: ('Hello', 42)", "name": "exampleFunction", "role": "function"},
    ]
    functions = [example_function_jsonschema]
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 111



def test_function_role(model_tag: str, example_function_jsonschema: dict):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [
        {"content": "Debug bot.", "role": "system"},
        {"content": "example return: ('Hello', 42)", "name": "exampleFunction", "role": "function"},
    ]
    functions = [example_function_jsonschema]
    assert tokenizer.count_functions_tokens(functions) == 55
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 78


def test_function_role_systemless(model_tag: str, example_function_jsonschema: dict):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [
        {"content": "example return: ('Hello', 42)", "name": "exampleFunction", "role": "function"},
    ]
    functions = [example_function_jsonschema]
    assert tokenizer.count_functions_tokens(functions) == 55
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 75


def test_functioncall_message(model_tag: str, example_function_jsonschema: dict):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [
        {"content": "Debug bot.", "role": "system"},
        {
            "content": None,
            "function_call": {
                "name": "exampleFunction",
                "arguments": '{\n  "param1": "Hello",\n  "param2": 42\n}',
            },
            "role": "assistant",
        },
    ]
    functions = [example_function_jsonschema]
    assert tokenizer.count_functions_tokens(functions) == 55
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 91


def test_functioncall_message_systemless(model_tag: str, example_function_jsonschema: dict):
    tokenizer = Totokenizer.from_model(model_tag)
    simple_chat: Chat = [
        {
            "content": None,
            "function_call": {
                "name": "exampleFunction",
                "arguments": '{\n  "param1": "Hello",\n  "param2": 42\n}',
            },
            "role": "assistant",
        },
    ]
    functions = [example_function_jsonschema]
    assert tokenizer.count_functions_tokens(functions) == 55
    assert tokenizer.count_chatml_tokens(simple_chat, functions) == 88


# TODO: function that accepts no parameters {"type": "object", "properties": {}}
