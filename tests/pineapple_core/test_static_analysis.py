from contextlib import redirect_stdout
import io
from pineapple_core.core.node import node
from pineapple_nodes.nodes.flow_nodes import sequence_node


@node(module="test", name="NodeThatShouldBeAutotriggerable")
def should_be_autotrigger_node() -> int:
    return 22


@node(module="test", name="NodeThatTakesSingleInput")
def takes_single_input_node(a: int):
    pass


def test_static_analysis():
    sequence = sequence_node()

    with sequence.step("test1") as first_step:
        first_step.dummy = should_be_autotrigger_node()
        first_step.dummy2 = takes_single_input_node()
        first_step.dummy_with_bad_name_node = takes_single_input_node()
        first_step.dummy_with_non_connected_input = takes_single_input_node()

        first_step.dummy2.connect_input(a=first_step.dummy)
        first_step.dummy2.connect_flow(first_step.dummy_with_bad_name_node)
        first_step.dummy2.connect_flow(first_step.dummy_with_non_connected_input)

        first_step.dummy3 = should_be_autotrigger_node()
        first_step.dummy2.connect_flow(first_step.dummy3)
        first_step.dummy_with_bad_name_node.connect_input(a=first_step.dummy3)

        first_step << first_step.dummy2

    f = io.StringIO()
    with redirect_stdout(f):
        sequence.trigger()
    stdout = f.getvalue().split("\n")
    assert (
        "[WARNING] Node test.NodeThatShouldBeAutotriggerable(test1.dummy)"
        + " is never triggered nor autotriggerable (needed by "
        + "test.NodeThatTakesSingleInput(test1.dummy2))"
    ) in stdout
    assert (
        "[WARNING] Node 'test.NodeThatTakesSingleInput(test1.dummy_with_non_connected_input)'"
        " has empty NodeInput 'Input[a](accepts=<class 'int'>, "
        "bind=None, hidden=False, optional=False, value=None)'"
    ) in stdout
    assert (
        "[WARNING] A Node instance shouldn't end with _node (on test1.dummy_with_bad_name_node)"
        in stdout
    )
