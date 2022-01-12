from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFT


def controlled_multiplier_gate(x_size, b_size):
    c = QuantumRegister(1, 'c')
    x = QuantumRegister(x_size, 'x')
    b = QuantumRegister(b_size, 'b')

    cr = QuantumCircuit(c, x, b)

    print(cr.draw())


controlled_multiplier_gate(2, 2)


def swap_reg(size):
    x = QuantumRegister(size, 'x')
    b = QuantumRegister(size, 'b')
    circuit = QuantumCircuit(x, b)
    circuit.swap(x, b)
    return circuit

def c_swap_register(size):
    c = QuantumRegister(1, 'c')
    x = QuantumRegister(size, 'x')
    b = QuantumRegister(size, 'b')

    circuit = QuantumCircuit(c, x, b)

    c_swap_gate = swap_reg(size).to_gate(label="SWAP").control(1)
    circuit.append(c_swap_gate, range(2*size+1))

    return circuit

