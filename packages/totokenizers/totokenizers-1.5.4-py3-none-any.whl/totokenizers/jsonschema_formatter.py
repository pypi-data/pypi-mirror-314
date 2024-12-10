import json
import textwrap


def _format_tool(tool):
    """https://gist.github.com/CGamesPlay/dd4f108f27e2eec145eedf5c717318f5"""

    def resolve_ref(schema):
        if schema.get("$ref") is not None:
            ref = schema["$ref"][14:]
            schema = json_schema["definitions"][ref]
        return schema

    def format_schema(schema, indent):
        schema = resolve_ref(schema)
        if "enum" in schema:
            return _format_enum(schema, indent)
        elif schema["type"] == "object":
            return format_object(schema, indent)
        elif schema["type"] == "integer":
            return "number"
        elif schema["type"] in ["string", "number"]:
            return schema["type"]
        elif schema["type"] == "array":
            return format_schema(schema["items"], indent) + "[]"
        else:
            raise ValueError("unknown schema type " + schema["type"])

    def _format_enum(schema, indent):
        return " | ".join(json.dumps(o) for o in schema["enum"])

    def format_object(schema, indent):
        result = "{\n"
        if "properties" not in schema or len(schema["properties"]) == 0:
            if schema.get("additionalProperties", False):
                return "object"
            return None
        for key, value in schema["properties"].items():
            value = resolve_ref(value)
            value_rendered = format_schema(value, indent + 1)
            if value_rendered is None:
                continue
            if "description" in value and indent == 0:
                for line in textwrap.dedent(value["description"]).strip().split("\n"):
                    result += f"{'  '*indent}// {line}\n"
            optional = "" if key in schema.get("required", {}) else "?"
            comment = (
                ""
                if value.get("default") is None
                else f" // default: {format_default(value)}"
            )
            result += f"{'  '*indent}{key}{optional}: {value_rendered},{comment}\n"
        result += ("  " * (indent - 1)) + "}"
        return result

    def format_default(schema):
        v = schema["default"]
        if schema["type"] == "number":
            return f"{v:.1f}" if float(v).is_integer() else str(v)
        else:
            return str(v)

    try:
        json_schema = tool["parameters"]
    except KeyError:
        tool = tool["function"]
        json_schema = tool["parameters"]
    result = f"// {tool['description']}\ntype {tool['name']} = ("
    formatted = format_object(json_schema, 0)
    if formatted is not None:
        result += "_: " + formatted
    result += ") => any;\n\n"
    return result


class FunctionJSONSchema:
    def __init__(self, functions: list[dict]):
        self.functions = functions

    def to_typescript(self) -> str:
        return "".join(_format_tool(f) for f in self.functions)
