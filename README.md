# Pineapple

Pineapple is a framework allowing you to create and chain nodes to execute a program.

## Introduction

Pineapple is a test framework designed to allow the construction of high level tests across the platform. Tests are made up of a collection of "nodes" which are linked together to control the flow of execution.

## Installation

You just have to clone this repository and install it using the command
```bash
pip install .
```

## Usage

```python
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
```

This example shows how to implement a password-checker using Pineapple

## Licensing

Pineapple uses the MIT license, you can find more details about it [here](LICENSE)

## Contributing

You can find more details about contributions [here](CONTRIBUTING.md)
