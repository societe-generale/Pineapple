import pytest

from pineapple_core.core.node import node, wrap
from pineapple_core.core.node_output import NodeOutput
from pineapple_core.core.types import Any
from pineapple_nodes.nodes.flow_nodes import null_node, format_exception_node
from pineapple_core.core.exceptions import (
    NoCallbacksError,
    CallbackManagerNotFoundError,
)


@node(module="test", name="DummyData", autotrigger=True)
def dummy_data_node() -> int:
    return 22


@node(module="test", name="ExtensibleNode")
def extensible_node(*args: Any, **kwargs: Any) -> {"out": int, "e": int}:
    return wrap({"e": sum(kwargs.values()), "out": 666})


def test_add_and_remove_callback():
    success_probe = ":("

    def on_trigger_callback(node):
        nonlocal success_probe
        success_probe = node.id

    original = null_node()
    original.id = "success_probe_ok"
    original.on.trigger.add(on_trigger_callback)
    original.trigger()

    assert success_probe == original.id

    success_probe = ":)"
    original.on.trigger.remove(on_trigger_callback)
    original.trigger()

    assert success_probe == ":)"

    original.on.trigger.add(on_trigger_callback)
    original.trigger()

    assert success_probe == original.id

    success_probe = ">:("
    original.on.trigger.remove_all()
    original.trigger()

    assert success_probe == ">:("


def test_callback_copy():
    logs = []

    def on_add_output_callback(node, node_output):
        node.mirror.add_output(node_output)

    def mirror_on_add_output_callback(node, node_output):
        logs.append(f"add_output({node.id}, {node_output.name})")

    def mirror_on_after_flow_callback(node, flow):
        logs.append(f"after_flow({node.id}, {flow.name})")

    def mirror_on_before_flow_callback(node, flow):
        logs.append(f"before_flow({node.id}, {flow.name})")

    def on_connect_flow_callback(node, flow):
        node.mirror.connect_flow(flow.node, flow.name)
        node.mirror.get_flow(flow.name).priority = flow.priority

    def mirror_on_connect_flow_callback(node, flow):
        logs.append(f"connect_flow({node.id}, {flow.name})")

    def on_connect_input_callback(node, node_input, node_output):
        kwargs = {node_input.name: node_output}
        node.mirror.connect_input(**kwargs)

    def mirror_on_connect_input_callback(node, node_input, node_output):
        logs.append(f"connect_input({node.id}, {node_input.name}, {node_output.name})")

    def mirror_on_flow_failure_callback(node, flow, exception):
        logs.append(f"flow_failure({node.id}, {flow.name}, {exception})")

    def on_set_input_value_callback(node, node_input, value):
        on_connect_input_callback(node, node_input, value)

    def mirror_on_set_input_value_callback(node, node_input, value):
        logs.append(f"set_input_value({node.id}, {node_input.name}, {value})")

    def on_trigger_callback(node):
        node.mirror.trigger()

    def mirror_on_trigger_callback(node):
        logs.append(f"trigger({node.id})")

    def mirror_on_trigger_input_callback(node, node_input, triggered_node):
        logs.append(f"trigger_input({node.id}, {node_input.name}, {triggered_node.id})")

    original = extensible_node()
    original.id = "original"

    original.on.add_output.add(on_add_output_callback, mirror_on_add_output_callback)
    original.on.after_flow.add(mirror_on_after_flow_callback)
    original.on.before_flow.add(mirror_on_before_flow_callback)
    original.on.connect_flow.add(
        on_connect_flow_callback, mirror_on_connect_flow_callback
    )
    original.on.connect_input.add(
        on_connect_input_callback, mirror_on_connect_input_callback
    )
    original.on.flow_failure.add(mirror_on_flow_failure_callback)
    original.on.set_input_value.add(
        on_set_input_value_callback, mirror_on_set_input_value_callback
    )
    original.on.trigger.add(on_trigger_callback, mirror_on_trigger_callback)
    original.on.trigger_input.add(mirror_on_trigger_input_callback)

    original.mirror = extensible_node()
    original.mirror.id = "mirror"
    original.mirror.on = original.on.copy()
    original.mirror.on.add_output = mirror_on_add_output_callback
    original.mirror.on.connect_flow = mirror_on_connect_flow_callback
    original.mirror.on.connect_input = mirror_on_connect_input_callback
    original.mirror.on.set_input_value = mirror_on_set_input_value_callback
    original.mirror.on.trigger = mirror_on_trigger_callback

    next_step = null_node()
    original.connect_flow(next_step)

    autotrigger_step = dummy_data_node()
    autotrigger_step.id = "dummy"
    original.connect_input(d=autotrigger_step)

    fail_step = format_exception_node()
    fail_step.connect_input(exception_name="FakeError", string="This is a fake error")
    original.connect_flow(fail_step)

    original.connect_input(a=1, b=2, c=3)
    original.add_output(NodeOutput(original, "e", int))

    original.trigger()

    assert original["out"].get() == 666 and original.mirror["out"].get() == 666
    assert original["e"].get() == 28 and original.mirror["e"].get() == 28
    assert logs == [
        "connect_flow(mirror, 0)",
        "connect_flow(original, 0)",
        "connect_input(mirror, d, out)",
        "connect_input(original, d, out)",
        "connect_flow(mirror, 1)",
        "connect_flow(original, 1)",
        "set_input_value(mirror, a, 1)",
        "set_input_value(original, a, 1)",
        "set_input_value(mirror, b, 2)",
        "set_input_value(original, b, 2)",
        "set_input_value(mirror, c, 3)",
        "set_input_value(original, c, 3)",
        "add_output(mirror, e)",
        "add_output(original, e)",
        "trigger(mirror)",
        "trigger_input(mirror, d, dummy)",
        "before_flow(mirror, 0)",
        "after_flow(mirror, 0)",
        "before_flow(mirror, 1)",
        "flow_failure(mirror, 1, This is a fake error)",
        "after_flow(mirror, 1)",
        "trigger(original)",
        "trigger_input(original, d, dummy)",
        "before_flow(original, 0)",
        "after_flow(original, 0)",
        "before_flow(original, 1)",
        "flow_failure(original, 1, This is a fake error)",
        "after_flow(original, 1)",
    ]


def test_no_callbacks_error():
    dummy_node = null_node()
    with pytest.raises(NoCallbacksError):
        dummy_node.on.trigger()


def test_non_existant_callback_manager_get():
    dummy_node = null_node()
    with pytest.raises(CallbackManagerNotFoundError):
        dummy_node.on.dummy_callback = lambda x: x
