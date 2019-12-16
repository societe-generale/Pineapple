from pineapple_nodes.nodes.flow_nodes import sequence_node
from pineapple_core.core.node import node, wrap
from pineapple_nodes.utils import build_int_equals_check, build_list_check
from pineapple_nodes.nodes.assertion_nodes import check_http_code


def test_list_check():
    input_list = [{"key": "a"}, {"key": "b"}, {"key": "c"}]
    list_check_node = build_list_check(input_list, "key", "b")
    list_check_false_node = build_list_check(input_list, "key", "d")

    test_sequence_node = sequence_node()
    test_sequence_node.connect_flow(list_check_node)
    test_sequence_node.connect_flow(list_check_false_node)

    test_sequence_node.trigger()

    assert list_check_node.result()["out"]["result"]
    assert list_check_node.result()["out"]["message"] == "Does key:b appear in " \
                                                         "[{'key': 'a'}, {'key': 'b'}," \
                                                         " {'key': 'c'}]"
    assert not list_check_false_node.result()["out"]["result"]
    assert list_check_false_node.result()["out"]["message"] == "Does key:d appear in " \
                                                               "[{'key': 'a'}, {'key': 'b'}," \
                                                               " {'key': 'c'}]"


def test_basic_assertion():
    equals_check_node = build_int_equals_check(1, 2, "{} is equal to {}")
    equals_check_true_node = build_int_equals_check(2, 2, "{} is equal to {}")

    test_sequence_node = sequence_node()
    test_sequence_node.connect_flow(equals_check_node)
    test_sequence_node.connect_flow(equals_check_true_node)

    test_sequence_node.trigger()

    assert not equals_check_node.result()["out"]["result"]
    assert equals_check_node.result()["out"]["message"] == "1 is equal to 2"
    assert equals_check_true_node.result()["out"]["result"]
    assert equals_check_true_node.result()["out"]["message"] == "2 is equal to 2"


def test_http_checker():
    http_200_node = http_test_node()
    http_200_node.connect_input(code=200)
    http_201_node = http_test_node()
    http_201_node.connect_input(code=201)
    http_check = check_http_code(http_200_node, 200)
    http_check_false = check_http_code(http_201_node, 204)

    test_sequence_node = sequence_node()
    test_sequence_node.connect_flow(http_check)
    test_sequence_node.connect_flow(http_check_false)

    test_sequence_node.trigger()

    assert http_check.result()["out"]["result"]
    assert not http_check_false.result()["out"]["result"]


http_result = {
    "_HttpCode": int
}


@node(module="Test", name="HttpTestNode", autotrigger=True)
def http_test_node(code: int) -> http_result:
    return wrap({"_HttpCode": code})
