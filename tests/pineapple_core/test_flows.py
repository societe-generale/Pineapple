from pineapple_core.core.node import node
from pineapple_nodes.nodes.flow_nodes import null_node


def put_number_inside(node, number):
    node.magic_number = number


@node(
    module="test",
    name="NodeThatContainsAMagicNumber",
    helper_function=put_number_inside,
)
def magic_number_node():
    pass


def test_flow_priorities():
    execution_order = []

    def on_trigger_callback(node):
        execution_order.append(node.magic_number)

    seq = null_node()

    first = magic_number_node(1)
    first.on.trigger = on_trigger_callback
    second = magic_number_node(2)
    second.on.trigger = on_trigger_callback
    third = magic_number_node(3)
    third.on.trigger = on_trigger_callback
    fourth = magic_number_node(4)
    fourth.on.trigger = on_trigger_callback
    fifth = magic_number_node(5)
    fifth.on.trigger = on_trigger_callback

    seq.connect_flow(fourth, "4")
    seq.connect_flow(second, "2")
    seq.connect_flow(fifth, "5")
    seq.connect_flow(first, "1")
    seq.connect_flow(third, "3")

    seq.trigger()

    assert execution_order == [4, 2, 5, 1, 3]
    execution_order.clear()

    for _ in range(4):
        seq.get_flow("1").increase_priority()
        seq.get_flow("3").increase_priority()
    seq.get_flow("2").increase_priority()
    for _ in range(2):
        seq.get_flow("4").decrease_priority()
        seq.get_flow("5").decrease_priority()

    seq.trigger()

    assert execution_order == [1, 2, 3, 4, 5]


def test_flow_dump():
    dummy = null_node()
    dummy.id = "dummy"
    dummy2 = null_node()
    dummy2.id = "dummy2"
    dummy.connect_flow(dummy2, "test_flow")

    assert dummy.get_flow("test_flow").dump() == {
        "name": "test_flow",
        "node": "dummy2",
        "priority": 1,
    }


def test_flow_copy():
    dummy = null_node()
    dummy.id = "dummy"
    dummy2 = null_node()
    dummy2.id = "dummy2"
    dummy.connect_flow(dummy2, "test_flow")

    flow_ref = dummy.get_flow("test_flow")
    flow_ref.pretty_name = "pretty flow"
    flow_copy = flow_ref.copy()
    assert flow_ref.name == flow_copy.name
    assert flow_ref.node == flow_copy.node
    assert flow_ref.priority == flow_copy.priority
    assert flow_ref.pretty_name == flow_copy.pretty_name


def test_flow_repr():
    dummy = null_node()
    dummy.id = "dummy"
    dummy2 = null_node()
    dummy2.id = "dummy2"
    dummy.connect_flow(dummy2, "test_flow")

    assert (
        dummy.get_flow("test_flow").__repr__()
        == "Flow(name='test_flow', priority=1, node=Flow.Null(dummy2))"
    )
