from pineapple_nodes.nodes import comparison_nodes, flow_nodes, io_nodes

print("=================================")
input_f = io_nodes.input_node()
input_f.connect_input(prompt="Password ? ")
equals_f = comparison_nodes.equals_node()
print_f = io_nodes.print_node()
print_f.connect_input(a="Was the password good : {}")
if_f = flow_nodes.if_node()
good_password_f = io_nodes.print_node()
good_password_f.connect_input(a="Wow you guessed the password, good job")
wrong_password_f = io_nodes.print_node()
wrong_password_f.connect_input(a="No the password is BAD")

equals_f.connect_input(a="azerty123")
equals_f.connect_input(b=input_f)
print_f.connect_input(equals_f)
if_f.connect_input(condition=equals_f)

input_f.connect_flow(print_f)
print_f.connect_flow(if_f)
if_f.connect_flow(good_password_f, True)
if_f.connect_flow(input_f, False)

input_f.trigger()
