import sys
import numpy as np

sys.path.append('.')

from src.quantum.gates.controlled_U_a_gate import c_U_a_gate
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from math import pi
from qiskit.circuit.library import PhaseGate

def a2jmodN(a, j, N):
    """Compute a^{2^j} (mod N) by repeated squaring"""
    for i in range(j):
        a = np.mod(a**2, N)
    return a


def changed_one_control_qubit(size, a, N):
    control = QuantumRegister(1)
    q = QuantumRegister(2 * size + 2)
    b = ClassicalRegister(2 * size)

    circuit = QuantumCircuit(control, q, b)

    circuit.x(q[0])

    for i in range(2 * size):
        circuit.h(control[0])

        circuit.append(c_U_a_gate(size, a2jmodN(a, i, N), N), range(2 * size + 3))

        for j in range(i):
            circuit.append(PhaseGate(((-pi) / 2 ** (i - j))).c_if(b[j], 1), [control[0]])

        circuit.h(control[0])
        circuit.swap(control[0], q[i])
        circuit.measure(q[i], b[i])
        circuit.swap(control[0], q[i])
        circuit.x(control[0]).c_if(b[i], 1)

    return circuit

def classic_one_control_qubit(size, a, N):
    control = QuantumRegister(1)
    q = QuantumRegister(2 * size + 2)
    b = ClassicalRegister(2 * size)

    circuit = QuantumCircuit(control, q, b)

    circuit.x(q[0])

    for i in range(2 * size):
        circuit.h(control[0])

        circuit.append(c_U_a_gate(size, a2jmodN(a, i, N), N), range(2 * size + 3))

        for j in range(i):
            circuit.append(PhaseGate(((-pi) / 2 ** (i - j))).c_if(b[j], 1), [control[0]])

        circuit.h(control[0])
        circuit.measure(control[0], b[i])
        circuit.x(control[0]).c_if(b[i], 1)

    return circuit


