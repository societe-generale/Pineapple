from pineapple_core.core.store import node_store
from pineapple_core.core.node import node
from pineapple_core.core.types import Any


@node(module="Test", name="AutoTriggerable", autotrigger=True)
def auto_triggerable(a: Any()) -> Any():
    return a


def test_nodes_registered_within_store():
    # GIVEN - WHEN
    a_node = auto_triggerable()
    a_node2 = auto_triggerable()
    # THEN
    assert a_node in node_store.values()
    assert a_node2 in node_store.values()
