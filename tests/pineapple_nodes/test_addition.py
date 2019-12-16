from io import StringIO
from contextlib import redirect_stdout
from pineapple_nodes.nodes import io_nodes, math_nodes


def test_addition_scenario():
    print("=================================")
    add_f = math_nodes.add_node()
    print_f = io_nodes.print_node()

    add_f.connect_input(a=22, b=11)
    print_f.connect_input(22, 11, add_f, a="Result of = {} + {} = {}")

    capturing_output = StringIO()
    with redirect_stdout(capturing_output):
        print_f.trigger()
        saved_output = capturing_output.getvalue()
    assert "Result of = 22 + 11 = 33" in saved_output
