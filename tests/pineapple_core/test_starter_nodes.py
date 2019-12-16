from pineapple_core.core.node import node


@node(module="Test", name="AppendToList", autotrigger=False)
def non_auto_appending_to_list(lisst: list, value: str) -> list:
    lisst.append(value)
    return lisst


@node(module="Test", name="AppendToList", autotrigger=True)
def auto_appending_to_list(lisst: list, value: str) -> list:
    lisst.append(value)
    return lisst


def test_order_respected_in_only_non_autotrigger():
    # GIVEN
    expected_list_order = ["intruder", "second", "first"]
    list_order = list()
    appending_node_first = non_auto_appending_to_list()
    appending_node_first.connect_input(lisst=list_order, value="first")

    appending_node_second = non_auto_appending_to_list()
    appending_node_second.connect_input(lisst=list_order, value="second")

    appending_node_intruder = non_auto_appending_to_list()
    appending_node_intruder.connect_input(lisst=list_order, value="intruder")

    appending_node_intruder.connect_flow(appending_node_second)
    appending_node_second.connect_flow(appending_node_first)
    # WHEN
    appending_node_intruder.trigger()
    # THEN
    assert list_order == expected_list_order
