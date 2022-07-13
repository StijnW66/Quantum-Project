# Shor's Algorithm using 2n + 3 Qubits.

## Description
This project contains a 2n + 3 Qubit implementation of Shor's algorithm based on this [paper](https://arxiv.org/abs/quant-ph/0205095)

The [Qiskit](https://qiskit.org/) sdk is used to build the Quantum Circuit and [Qutech's Quantum Inspire](https://www.quantum-inspire.com/) platform is used to run a simulation. (Note that there is a time limit. For larger simulations a local simulator can be used).

## File structure
[./src/quantum/gates](./src/quantum/gates) defines the gates (building blocks) of the circuit such as the [Adder](./src/quantum/gates/adder_gate.py), [Modular Adder](./src/quantum/gates/modular_adder_gate.py), [Controlled Multiplier](./src/quantum/gates/controlled_multiplier_gate.py), [Controlled Swap](./src/quantum/gates/controlled_swap_gate.py). Which are used to finally construct the [Controlled U Gate](./src/quantum/gates/controlled_U_a_gate.py).

With the Controlled U Gate the Quantum Phase Estimation circuit can be built: [./src/quantum/gates/control_qubits.py](./src/quantum/gates/control_qubits.py) contains the code for this circuit wiht 2n control qubits and [./src/quantum/gates/one_control_qubit.py](./src/quantum/gates/one_control_qubit.py) contains the code using the "single control qubit trick".

Finally some postprocessing is performed in [./src/quantum/shor_algorithm.py](./src/quantum/shor_algorithm.py) to succesfully factorize a number into its prime factors.

## Contributors:
- Stijn van de Water
- Andrzej Rubio Bizcaino
- Pepijn Habing
- Floris Scharmer
