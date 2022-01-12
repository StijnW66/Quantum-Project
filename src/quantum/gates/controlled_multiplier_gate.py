from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFT


def controlled_multiplier_gate(x_size, b_size):
    c = QuantumRegister(1, 'c')
    x = QuantumRegister(x_size, 'x')
    b = QuantumRegister(b_size, 'b')

    cr = QuantumCircuit(c, x, b)

    print(cr.draw())


controlled_multiplier_gate(2, 2)
