from pineapple_core.core.node import Node
from pineapple_core.core.node_input import NodeInput
from pineapple_core.core.node_output import NodeOutput
from pineapple_core.core.exceptions import HiddenNodeInputConnectError
from .test_base import uuid_regex
from klotan import match
from klotan import criterias

import pytest

dummy_node = Node(lambda x: x, "Dummy", "Node", False)


def test_that_check_nodeinput_fallback_values():
    nice_input = NodeInput(dummy_node, "niceinput", str, False)
    nice_input.set("This is a fallback value")
    assert nice_input.get() == "This is a fallback value"
    str_output = NodeOutput(dummy_node, "stroutput", str)  # The famous creator of C++
    str_output.set("This is not a fallback value")
    nice_input.connect(str_output)
    assert nice_input.get() == "This is not a fallback value"


def test_that_check_nodeinput_connect():
    cool_input = NodeInput(dummy_node, "coolinput", str, False)
    cool_output = NodeOutput(dummy_node, "cooloutput", str)
    cool_input.connect(cool_output)
    mean_input = NodeInput(dummy_node, "meaninput", str, True)
    with pytest.raises(HiddenNodeInputConnectError):
        mean_input.connect(cool_output)


def test_that_check_nodeinput_dump():
    beautiful_input = NodeInput(dummy_node, "dump_test", int)
    beautiful_input.set(666)
    ugly_output = NodeOutput(dummy_node, "subdump_test", int)
    beautiful_input.connect(ugly_output)
    dump_match = match.match(
        {
            "id": criterias.is_type(str)
            & criterias.regex(uuid_regex)
            & criterias.equals(str(beautiful_input.id)),
            "type": criterias.equals("NodeInput"),
            "name": criterias.equals("dump_test"),
            "input_type": criterias.equals(str(int)),
            "parent": criterias.is_type(str)
            & criterias.regex(uuid_regex)
            & criterias.equals(str(beautiful_input.node.id)),
            "value": criterias.equals(666),
            "hidden": criterias.equals(False),
            "connected_output": criterias.is_type(str)
            & criterias.regex(uuid_regex)
            & criterias.equals(str(ugly_output.id)),
        },
        beautiful_input.dump(),
    )
    print(beautiful_input.dump())
    print(dump_match.to_string())
    assert dump_match.is_valid()


def test_that_check_nodeinput_repr():
    terrible_input = NodeInput(dummy_node, "aterriblename", str)
    terrible_input.set("Whale")

    assert str(terrible_input) == (
        "Input[aterriblename](accepts=<class 'str'>, bind=None, "
        "hidden=False, optional=False, value=Whale)"
    )
