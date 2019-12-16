from pineapple_core.core.node import Node, node, wrap


def forward_arg_helper(self, number):
    self.number = number


@node(
    module="Test",
    name="NodeThatReturnsANumber",
    autotrigger=True,
    helper_function=forward_arg_helper,
)
def number_node(self: Node) -> int:
    return self.number


@node(module="Test", name="NodeThatTestsDictValues")
def check_values_in_dict_node(dictionary: dict) -> bool:
    return dictionary["a"] == 11 and dictionary["b"][1] == 22


def test_that_checks_input_wrapping():
    eleven = number_node(11)
    twentytwo = number_node(22)
    check = check_values_in_dict_node()
    check.connect_input(dictionary=wrap({"a": eleven, "b": [33, twentytwo]}))
    check.trigger()
    assert check["out"].get() is True
