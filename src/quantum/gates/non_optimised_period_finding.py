import sys

from qiskit.circuit.library import QFT

sys.path.append('.')

from src.quantum.gates.controlled_U_a_gate import c_U_a_gate
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


def period_finding_routine(size, a, N):
    control = QuantumRegister(2 * size)
    q = QuantumRegister(2 * size + 2)
    m = ClassicalRegister(2 * size)

    circuit = QuantumCircuit(control, q, m)

    circuit.x(q[0])

    for i in range(2 * size):
        circuit.h(control[i])

    for i in range(2 * size):
        # Add U here
        U_gate = c_U_a_gate(size, a**2**i, N)
        circuit.append(U_gate, [control[2*size-1-i]] + q[0: 2 * size + 2])

    circuit.append(QFT(num_qubits=2*size, approximation_degree=0, do_swaps=True, inverse=True, insert_barriers=False, name='iqft'), control[0:2*size])

    circuit.measure(control[0:2*size], m[0:2*size])

    return circuit



circuit = period_finding_routine(len(bin(15)) - 2, 4, 15)
print(circuit.draw())
