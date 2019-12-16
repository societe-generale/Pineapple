from pineapple_core.core.node import node, Node


@node(module="Debug", name="StillWaiting")
def still_waiting_node(i: int):
    print("Still waiting", i)


@node(module="Debug", name="Success")
def success_node():
    print("You did it !")


@node(module="Debug", name="StupidNode")
def stupid_node(self: Node, i: int):
    for flow in self.flows:
        flow.disable()
    self.get_flow(i).enable()
    print("Enable", i)
    self.inputs["i"].value = i + 1


def test_that_checks_priority_stacking():
    d_trigger_count = 0

    def increase_d_trigger_count(node):
        nonlocal d_trigger_count
        d_trigger_count += 1

    a = stupid_node()
    a.id = "a"
    a.connect_input(i=1)
    b = still_waiting_node()
    b.id = "b"
    b.connect_input(i=1)
    c = still_waiting_node()
    c.id = "c"
    c.connect_input(i=2)
    d = success_node()
    d.id = "d"

    d.on.trigger.add(increase_d_trigger_count)

    a.connect_flow(b, 1)
    a.connect_flow(c, 2)
    a.connect_flow(d, 3)
    b.connect_flow(a)
    c.connect_flow(a)

    a.trigger()

    assert d_trigger_count == 1
