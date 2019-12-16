import pytest
from pineapple_nodes.nodes.reporting_nodes import report_node
from pineapple_nodes.nodes.flow_nodes import sequence_node
from pineapple_nodes.utils import build_int_equals_check


@pytest.mark.parametrize("result_bool", [True, False])
def test_false_report(result_bool):
    equals_node_true = build_int_equals_check(2, 2, "Does {} equal {}")
    other_int = 2 if result_bool else 1
    other_equals_node = build_int_equals_check(2, other_int, "Does {} equal {}")
    equality_report_node = report_node()
    equality_report_node.connect_input(equals_node_true, other_equals_node)

    test_sequence_node = sequence_node()
    test_sequence_node.connect_flow(equals_node_true)
    test_sequence_node.connect_flow(other_equals_node)
    test_sequence_node.connect_flow(equality_report_node)

    test_sequence_node.trigger()

    assert result_bool == equality_report_node.result()["passed"]
    assert "Does 2 equal 2: True" in equality_report_node.result()["report"]
    assert f"""Does 2 equal {other_int}: {result_bool}""" in equality_report_node.result()["report"]
