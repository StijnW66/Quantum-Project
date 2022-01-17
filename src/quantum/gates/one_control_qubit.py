import sys
sys.path.append('.')

from src.quantum.gates.controlled_U_a_gate import c_U_a_gate
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

def one_control_qubit(size, a, N):
    control = QuantumRegister(1)
    q = QuantumRegister(size)
    b = ClassicalRegister(2*size)

    circuit = QuantumCircuit(control, q, b)


    for i in range(2*size):
        circuit.h(control[0])

        # Add U here
        U_gate = mock_Circuit(size)
        gate = U_gate.to_gate().control(1)
        circuit.append(c_U_a_gate(size, a, N), range(size+1))

        for j in range(i):
            circuit.p(-((2*3.14)/2**(j+2)), control[0]).c_if(b[j], 1)

        circuit.h(control[0])
        circuit.measure(control[0], b[i])
        circuit.x(control[0]).c_if(b[i], 1)

    return circuit

def mock_Circuit(size):
    q = QuantumRegister(size)
    circuit = QuantumCircuit(q)
    return circuit

circuit = one_control_qubit(2, 4, 15)
print(circuit.draw())

