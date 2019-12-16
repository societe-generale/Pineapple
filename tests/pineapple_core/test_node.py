from pineapple_core.core.node import wrap, node, copy_scenario_state
from pineapple_core.core.types import Any
from pineapple_core.core.node_output import NodeOutput
from klotan.match import OptionalKey
from pineapple_core.core.exceptions import (
    InvalidNodeFunctionReturnTypeError,
    NodeDoesNotAllowArgsError,
    NodeDoesNotAllowKwargsError,
    ResultOutputMismatchError,
    InexistantOutputResultError,
    NodeOutputNotFoundError,
    NoOutputError,
    AmbiguousNodeOutputError,
)

import pytest


@node(module="Test", name="VeryDumbDummy")
def very_dummy_node():
    pass


@node(module="Test", name="DumbAutotrigger", autotrigger=True)
def dumb_autotrigger_node() -> int:
    return 22


@node(module="Test", name="YES")
def dummy_node() -> str:
    return "YES"


@node(module="Test", name="OptionalOutput")
def dummy_with_optional_output_node() -> {"a": int, OptionalKey("b"): str}:
    return wrap({"a": 5})


@node(module="Test", name="TupleOutput")
def dummy_with_tuple_output() -> (int, int, int, int):
    return wrap((1, 2, 3, 4))


@node(module="Test", name="ListOutput")
def dummy_with_list_output() -> [str, str, str]:
    return wrap(["Sword", "Shield", "TREBUCHET"])


@node(module="Test", name="DictOutput")
def dummy_with_dict_output() -> {"first": int, "second": str, "third": str}:
    return wrap({"first": 3, "second": "Hello", "third": "AB"})


def dummy_with_invalid_output() -> 22:
    return 22


@node(module="Test", name="ConvenientNode", autotrigger=True)
def dummy_node_with_convenient_outputs() -> (int, str, bool):
    return wrap((1, "2", True))


@node(module="Test", name="DummyWithInputs")
def dummy_with_inputs_node(a: int, b: str, c: bool) -> (int, float):
    print("a", a, "b", b, "c", c)
    return wrap((a * 2 if c else a * 3, float(int(b, 16)) / 2.5))


@node(module="Test", name="ChaoticOutputs")
def dummy_with_chaotic_outputs(power: int):
    return wrap([x ** power for x in range(22)])


@node(module="Test", name="WrongAmountOfOutput")
def dummy_with_wrong_amount_of_outputs_node() -> [int, int]:
    return 22


@node(module="Test", name="InvalidOutput")
def dummy_with_wrong_outputs_node() -> {"a": int, "c": int}:
    return wrap({"a": 22, "b": 11})


@node(module="Test", name="NodeThatRaises")
def dummy_that_raises_node():
    raise RuntimeError("It fails!")


@node(module="Test", name="NodeWithAdditionalAttributes", super_attribute=22)
def dummy_with_additional_attributes():
    pass


@node(module="Test", name="NodeWithArgsAndKwargs")
def dummy_with_args_and_kwargs(*args: Any, **kwargs: Any):
    pass


fail_counter = 0


@node(module="Test", name="FailMultipleTimes")
def configured_fail_node(failures: int) -> str:
    global fail_counter
    if fail_counter >= failures:
        return "Passed"
    else:
        fail_counter += 1
        raise Exception("Test")


@node(module="Test", name="DummyWithoutArgs")
def dummy_without_args(a: int, b: int, c: int) -> (list):
    print("a", a, "b", b, "c", c)
    return [a, b, c]


@node(module="Test", name="DummyWithArgs")
def dummy_with_args(a: int, b: int, c: int, *args) -> (list):
    print("a", a, "b", b, "c", c, "args", *args)
    return [a, b, c, *args]


@node(module="Test", name="DummyWithKwargs")
def dummy_with_kwargs(a: int, b: int, c: int, *args, **kwargs) -> (list):
    print("a", a, "b", b, "c", c, "args", *args, "kwargs", kwargs)
    return [a, b, c, *args, kwargs]


def test_node_handle_multiple_connect_input():
    node_kwargs = dummy_with_kwargs()
    args1 = [1, 2, 3]
    args2 = [4, 5, 6]
    node_kwargs.connect_input(*args1)
    node_kwargs.connect_input(*args2)
    node_kwargs.trigger()

    assert node_kwargs["out"].get() == [4, 5, 6, {}]


@pytest.mark.parametrize("named_args,kwargs", [
    ([None, 2, 3], {}),
    ([1, 2, None], {}),
    ([1, None, 3], {}),
    ([None, 2, None], {}),
    ([None, None], {'b': 2}),
    ([1, None], {'b': 2}),
    ([None, 3], {'a': 1}),
    ([], {'a': None, 'b': 2, 'c': None})
])
def test_node_handle_none_args(named_args, kwargs):
    node_kwargs = dummy_with_kwargs()
    node_kwargs.connect_input(*named_args, **kwargs)
    node_kwargs.trigger()

    if kwargs == {}:
        assert node_kwargs["out"].get() == named_args + [{}]
    elif named_args == [1, None]:
        assert node_kwargs["out"].get() == [1, 2, None, {}]
    elif named_args == [None, 3]:
        assert node_kwargs["out"].get() == [1, None, 3, {}]
    else:
        assert node_kwargs["out"].get() == [None, 2, None, {}]


@pytest.mark.parametrize("named_args,kwargs", [
    ([1, 2, 3], {}),
    ([2, 3], {'a': 1}),
    ([], {'a': 1, 'b': 2, 'c': 3})
])
def test_node_handle_args(named_args, kwargs):
    node_no_args = dummy_without_args()
    node_no_args.connect_input(*named_args, **kwargs)
    node_no_args.trigger()

    node_args = dummy_with_args()
    node_args.connect_input(*named_args, 4, **kwargs)
    node_args.trigger()

    node_kwargs = dummy_with_kwargs()
    node_kwargs.connect_input(*named_args, **kwargs, e=4)
    node_kwargs.trigger()

    assert node_no_args["out"].get() == [1, 2, 3]
    assert node_args["out"].get() == [1, 2, 3, 4]
    assert node_kwargs["out"].get() == [1, 2, 3, {'e': 4}]


def test_node_retries_and_succeeds():
    # GIVEN
    failure_count = 2
    failure_node = configured_fail_node()
    failure_node.connect_input(failures=failure_count)
    failure_node.set_retries(2, 0.01)

    # WHEN
    failure_node.trigger()

    # THEN
    global fail_counter
    assert failure_node["out"].get() == "Passed"
    assert fail_counter == failure_count


def test_that_checks_node_creation():
    new_node = dummy_node()
    new_node.trigger()
    assert new_node["out"].get() == "YES"
    new_node = dummy_with_tuple_output()
    new_node.trigger()
    assert new_node[3].get() == 4
    new_node = dummy_with_list_output()
    new_node.trigger()
    assert new_node[2].get() == "TREBUCHET"
    new_node = dummy_with_dict_output()
    new_node.trigger()
    assert (
        new_node["second"].get()
        + " "
        + new_node["first"].get() * new_node["third"].get()
        == "Hello ABABAB"
    )
    with pytest.raises(InvalidNodeFunctionReturnTypeError):
        node(module="Test", name="InvalidOutput")(dummy_with_invalid_output)()


def test_that_checks_node_full_name():
    new_node = dummy_node()
    assert new_node.full_name() == f"Test.YES({new_node.id})"
    assert str(new_node) == new_node.__repr__()


def test_that_checks_node_dynamic_output_creation():
    new_node = dummy_with_chaotic_outputs()
    new_node.connect_input(power=3)
    for x in range(22):
        new_node.add_output(NodeOutput(new_node, x, int))
    new_node.trigger()
    assert new_node[11].get() == 1331


def test_that_checks_node_connect_input():
    new_node = dummy_with_inputs_node()
    convenient_node = dummy_node_with_convenient_outputs()
    new_node.connect_input(
        a=convenient_node[0], b=convenient_node[1], c=convenient_node[2]
    )
    new_node.trigger()
    assert new_node[0].get() == 2 and new_node[1].get() == 0.8


def test_get_non_existant_flow():
    dummy = dummy_node()

    assert dummy.get_flow("doesntexist") is None


def test_node_copy():
    dummy_origin = dummy_node()

    dummy = dummy_node()
    dummy.delay = 10
    dummy.retries = 3
    dummy.origin = dummy_origin

    dummy_copy = dummy.copy()

    attr_list = [
        "id",
        "module",
        "name",
        "function",
        "autotrigger",
        "allow_args",
        "allow_kwargs",
        "is_aware",
        "origin",
        "delay",
        "retries",
    ]

    for attr in attr_list:
        assert getattr(dummy, attr) == getattr(dummy_copy, attr)


def test_connect_args_kwargs_input():
    dummy = dummy_node()
    with pytest.raises(NodeDoesNotAllowArgsError):
        dummy.connect_input(1, 2, 3)
    with pytest.raises(NodeDoesNotAllowKwargsError):
        dummy.connect_input(a=1, b=2, c=3)


def test_automatic_flow_naming():
    dummy = dummy_node()
    dummy2 = dummy_node()
    dummy3 = dummy_node()
    dummy4 = dummy_node()
    dummy5 = dummy_node()

    dummy.connect_flow(dummy2)
    dummy.connect_flow(dummy3)
    dummy.connect_flow(dummy4)

    assert [flow.name for flow in dummy.flows] == [0, 1, 2]

    dummy.flows = []

    dummy.connect_flow(dummy2, 1)
    dummy.connect_flow(dummy3)
    dummy.connect_flow(dummy4, 5)
    dummy.connect_flow(dummy5)

    assert [flow.name for flow in dummy.flows] == [1, 2, 5, 3]


def test_function_result_bind_to_outputs_errors():
    dummy = dummy_with_wrong_amount_of_outputs_node()
    with pytest.raises(ResultOutputMismatchError):
        dummy.trigger()

    dummy2 = dummy_with_wrong_outputs_node()
    with pytest.raises(InexistantOutputResultError):
        dummy2.trigger()


def test_that_node_can_raise_exceptions():
    dummy = dummy_node()
    dangerous_dummy = dummy_that_raises_node()

    dummy.connect_flow(dangerous_dummy)

    with pytest.raises(RuntimeError):
        dummy.trigger()


def test_node_dump():
    dummy = dummy_node()
    dummy.id = "dummy"
    dummy["out"].id = "out"

    assert dummy.dump() == {
        "id": "dummy",
        "type": "Node",
        "module": "Test",
        "name": "YES",
        "autotrigger": False,
        "inputs": {},
        "outputs": {
            "out": {
                "id": "out",
                "type": "NodeOutput",
                "name": "out",
                "output_type": "<class 'str'>",
                "parent": "dummy",
                "value": None,
            }
        },
        "args_inputs": [],
        "kwargs_inputs": {},
        "flows": [],
    }


def test_get_optional_and_unknown_outputs():
    dummy = dummy_with_optional_output_node()
    with pytest.raises(NodeOutputNotFoundError):
        dummy["c"]


def test_extract_no_or_multiple_output():
    dummy = dummy_with_chaotic_outputs()

    dummy2 = very_dummy_node()
    dummy3 = dummy_with_tuple_output()

    with pytest.raises(NoOutputError):
        dummy.connect_input(power=dummy2)

    with pytest.raises(AmbiguousNodeOutputError):
        dummy.connect_input(power=dummy3)


def test_node_additional_attributes():
    dummy = dummy_with_additional_attributes()
    assert dummy.super_attribute == 22


def test_copy_scenario():
    outside_node = dummy_node()

    dummy = dummy_node_with_convenient_outputs()
    dummy2 = dummy_with_inputs_node()

    dummy2.connect_input(
        a=dummy[0], b=dummy[1], c=NodeOutput(outside_node, "weird", int)
    )

    dummy3 = very_dummy_node()
    dummy4 = dumb_autotrigger_node()
    dummy5 = dumb_autotrigger_node()

    dummy6 = dummy_with_args_and_kwargs()
    dummy6.connect_input(dummy4, x=dummy5)

    dummy2.connect_flow(dummy3)
    dummy3.connect_flow(dummy6)

    scenario_copy = copy_scenario_state(dummy2)

    assert dummy2.id == scenario_copy.id
    assert len(dummy2.flows) == len(scenario_copy.flows)
