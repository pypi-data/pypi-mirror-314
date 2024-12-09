from typing import Literal

from emp_agents.utils import get_function_schema


def simple_func(x: Literal["a", "b", "c"]) -> str:
    return "test"


def test_enums_in_schema():
    schema = get_function_schema(simple_func)
    assert schema["parameters"]["properties"]["x"]["enum"] == ["a", "b", "c"]
