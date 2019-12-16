from pineapple_core.core.types import SumType
from pineapple_core.utils.serialization import make_value_serializable
from pineapple_nodes.nodes.flow_nodes import SwitchNodeDefault


def test_serialization():
    assert make_value_serializable(3) == 3
    assert make_value_serializable("hello") == "hello"
    assert make_value_serializable(SwitchNodeDefault) == "__SWITCH_DEFAULT__"
    assert (
        make_value_serializable(SumType(int, str))
        == "SumType((<class 'int'>, <class 'str'>))"
    )
    assert make_value_serializable(int) == "<class 'int'>"
