from qiskit import QuantumRegister, QuantumCircuit


def swap_reg(size):
    # swaps registers x and b
    x = QuantumRegister(size, 'x')
    b = QuantumRegister(size, 'b')
    circuit = QuantumCircuit(x, b)
    circuit.swap(x, b)
    return circuit


def c_swap_register(size):
    # controlled SWAP of registers x and b
    c = QuantumRegister(1, 'c')
    x = QuantumRegister(size, 'x')
    b = QuantumRegister(size, 'b')

    circuit = QuantumCircuit(c, x, b)

    # Create controlled SWAP gate
    c_swap_gate = swap_reg(size).to_gate(label="SWAP").control(1)
    circuit.append(c_swap_gate, range(2 * size + 1))

    return circuit
