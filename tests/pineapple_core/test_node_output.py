from pineapple_core.core.node_output import NodeOutput
from pineapple_core.core.node import Node
from pineapple_core.core.exceptions import InvalidNodeOutputTypeError
from pineapple_core.core.types import Any, SumType
from .test_base import uuid_regex
from klotan import match
from klotan import criterias
import pytest
import typing

dummy_node = Node(lambda x: x, "Dummy", "Node", False)


def test_that_check_nodeoutput_typecheck():
    int_output = NodeOutput(dummy_node, "int_output", int)
    with pytest.raises(InvalidNodeOutputTypeError):
        int_output.set("hello")
    int_output.set(22)
    any_output = NodeOutput(dummy_node, "any_output", Any())
    any_output.set(lambda x: x)
    any_output.set(11)
    any_output.set("It works with anything")
    sumtype_output = NodeOutput(dummy_node, "none_output", SumType(bool, str))
    sumtype_output.set(True)
    sumtype_output.set("Goodbye")
    with pytest.raises(InvalidNodeOutputTypeError):
        sumtype_output.set(22)


def test_that_check_nodeoutput_value_getter():
    str_output = NodeOutput(dummy_node, "str_output", str)
    str_output.set("Strange string")
    assert str_output.get() == "Strange string"


def test_that_check_nodeoutput_dump():
    cool_output = NodeOutput(dummy_node, "dump_test", int)
    dump_match = match.match(
        {
            "id": criterias.is_type(str)
            & criterias.regex(uuid_regex)
            & criterias.equals(str(cool_output.id)),
            "type": criterias.equals("NodeOutput"),
            "name": criterias.equals("dump_test"),
            "output_type": criterias.equals(str(int)),
            "parent": criterias.is_type(str)
            & criterias.regex(uuid_regex)
            & criterias.equals(str(cool_output.node.id)),
            "value": criterias.equals(None),
        },
        cool_output.dump(),
    )
    print(cool_output.dump())
    print(dump_match.to_string())
    assert dump_match.is_valid()


def test_that_check_nodeoutput_repr():
    cooler_output = NodeOutput(dummy_node, "acoolname", str)
    assert str(cooler_output) == "Output[acoolname](type=<class 'str'>, value=None)"


def test_that_checks_multiple_nodeoutput_types():
    versatile_output = NodeOutput(dummy_node, "versatile_output", [int])
    versatile_output.set([1, 2, 3, 4])

    assert versatile_output.get()[0] == 1
    assert versatile_output.get()[1] == 2
    assert versatile_output.get()[2] == 3
    assert versatile_output.get()[3] == 4

    beautiful_output = NodeOutput(
        dummy_node,
        "beautiful_output",
        {"a": [int], "b": {"c": [[int]]}, "d": [{"e": str}]},
    )
    beautiful_output.set(
        {"a": [44], "b": {"c": [[22]]}, "d": [{"e": "hello"}, {"e": "goodbye"}]}
    )

    assert beautiful_output.get()["a"][0] == 44
    assert beautiful_output.get()["b"]["c"][0][0] == 22
    assert beautiful_output.get()["d"][0]["e"] == "hello"
    assert beautiful_output.get()["d"][1]["e"] == "goodbye"


def test_that_checks_invalid_output_type():
    wrong_output = NodeOutput(dummy_node, "wrong_output", [str])
    with pytest.raises(InvalidNodeOutputTypeError):
        wrong_output.set([22])

    wrong_output2 = NodeOutput(dummy_node, "wrong_output2", {"a": 1})
    with pytest.raises(RuntimeError):
        wrong_output2.set({"a": "no"})

    wrong_output3 = NodeOutput(dummy_node, "wrong_output3", [1])
    with pytest.raises(RuntimeError):
        wrong_output3.set(["yes"])


def test_typing_in_node_output():
    deprecated_output = NodeOutput(
        dummy_node, "deprecated_output", typing.Optional[int]
    )
    deprecated_output.set(22)
