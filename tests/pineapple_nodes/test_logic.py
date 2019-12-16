from pineapple_nodes.nodes.logic_nodes import and_node, or_node, false_node, true_node
from pineapple_nodes.nodes.flow_nodes import sequence_node


def test_and_node():
    true = true_node()
    false = false_node()
    and_check_false = and_node()
    and_check_false.connect_input(a=true)
    and_check_false.connect_input(b=false)
    and_check_true = and_node()
    and_check_true.connect_input(a=true)
    and_check_true.connect_input(b=true)

    test_sequence_node = sequence_node()
    test_sequence_node.connect_flow(and_check_false)
    test_sequence_node.connect_flow(and_check_true)

    test_sequence_node.trigger()

    assert not and_check_false["out"].get()
    assert and_check_true["out"].get()


def test_or_node():
    true = true_node()
    false = false_node()
    or_check_false = or_node()
    or_check_false.connect_input(a=false)
    or_check_false.connect_input(b=false)
    or_check_true = or_node()
    or_check_true.connect_input(a=false)
    or_check_true.connect_input(b=true)

    test_sequence_node = sequence_node()
    test_sequence_node.connect_flow(or_check_false)
    test_sequence_node.connect_flow(or_check_true)

    test_sequence_node.trigger()

    assert not or_check_false["out"].get()
    assert or_check_true["out"].get()
