from pineapple_core.core.node import node
from pineapple_core.core.store import node_store, model_store


@node(module="Tests", name="TestNode")
def test_node():
    pass


def test_nodes_registered_within_node_store_on_instanciation():
    # GIVEN - WHEN
    a_node = test_node()
    a_node2 = test_node()
    # THEN
    assert a_node in node_store.values()
    assert a_node2 in node_store.values()


def test_nodes_registered_within_model_store_on_declaration():
    # GIVEN
    module_name = "test"
    model_name = "testModelRegistered"
    compound_name = f"{module_name}.{model_name}"

    # WHEN
    @node(module=module_name, name=model_name)
    def random_node():
        pass

    # THEN
    assert compound_name in model_store.keys()
