import sys
sys.path.append('.')

from src.quantum.qi_runner import setup_QI, execute_circuit, print_results


from src.quantum.gates.controlled_U_a_gate import c_U_a_gate
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

def one_control_qubit(size, a, N):
    control = QuantumRegister(1)
    q = QuantumRegister(2*size + 2)
    b = ClassicalRegister(2*size)

    circuit = QuantumCircuit(control, q, b)

    for i in range(2*size):
        circuit.x(q[i])


    for i in range(2*size):
        circuit.h(control[0])

        circuit.append(c_U_a_gate(size, a**2**i, N), range(2*size+3))

        for j in range(i):
            circuit.p(-((2*3.14)/2**(j+2)), control[0]).c_if(b[j], 1)

        circuit.h(control[0])
        circuit.swap(control[0], q[i])
        circuit.measure(q[i], b[i])
        circuit.swap(control[0], q[i])
        circuit.x(control[0]).c_if(b[i], 1)

    return circuit


circuit = one_control_qubit(6, 4, 63)
print(circuit.draw())

setup_QI('tests')

print_results(execute_circuit(circuit, 50), circuit)



