from pineapple_nodes.nodes.flow_nodes import sequence_node, format_exception_node
from pineapple_nodes.nodes.io_nodes import print_node

sequence = sequence_node()

with sequence.step("first_step") as first_step:
    first_step.print = print_node()
    first_step.print.connect_input(a="Hello, I'm a first step")
    first_step << first_step.print

with sequence.step("second_step") as second_step:
    second_step.print = print_node()
    second_step.print.connect_input(a="Here comes the second step")
    second_step << second_step.print

with sequence.step("third_step") as third_step:
    third_step.print = print_node()
    third_step.print.connect_input(a="Now is the time for the third step")
    third_step.print2 = print_node()
    third_step.print2.connect_input(a="Still in the third step")
    third_step.print.connect_flow(third_step.print2)
    third_step << third_step.print

with sequence.step("fourth_step") as fourth_step:
    fourth_step.print = print_node()
    fourth_step.print.connect_input(a="I'm the fourth step")
    fourth_step << fourth_step.print

with sequence.step("fifth_step") as fifth_step:
    fifth_step.exception = format_exception_node()
    fifth_step.exception.connect_input(
        exception_name="ThingError",
        string="My goal is to raise errors"
    )
    first_step << fifth_step.exception

with sequence.step("sixth_step") as sixth_step:
    sixth_step.print = print_node()
    sixth_step.print.connect_input(a="Sixth step !")
    sixth_step << sixth_step.print

with sequence.failure_step() as failure_step:
    failure_step.clean = print_node()
    failure_step.clean.connect_input(a="I'm the cleaning step")
    failure_step << failure_step.clean

if __name__ == "__main__":
    sequence.trigger()
    print(f"I'm done executing the {len(sequence.flows)} steps")
