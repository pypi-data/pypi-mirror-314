import pytest

from totokenizers.jsonschema_formatter import FunctionJSONSchema


@pytest.fixture(scope="module")
def example_function_typescript():
    s = """// This is an example function
type exampleFunction = (_: {
// This is parameter 1
param1: string,
// This is parameter 2
param2?: number,
}) => any;\n\n"""
    return s


@pytest.fixture(scope="module")
def example_function2_typescript():
    s = """// Description of example function the AI will repeat back to the user
type function_name = (_: {
// description of function property 1: string
property1?: string,
// description of function property 2: string w enum
property2?: "enum_yes" | "enum_no",
}) => any;\n\n"""
    return s


def test_jsonschema_typescript_tranlation(example_function_jsonschema: dict, example_function_typescript: str):
    ts = FunctionJSONSchema([example_function_jsonschema]).to_typescript()
    assert ts == example_function_typescript


def test_jsonschema_typescript_tranlation2(example_function2_jsonschema: dict, example_function2_typescript: str):
    ts = FunctionJSONSchema([example_function2_jsonschema]).to_typescript()
    assert ts == example_function2_typescript
