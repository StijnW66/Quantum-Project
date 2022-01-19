import sys
sys.path.append('.')

from src.quantum.qi_runner import setup_QI, execute_circuit, print_results


from src.quantum.gates.controlled_U_a_gate import c_U_a_gate
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library import QFT

def control_qubits(size, a, N):
    control = QuantumRegister(2*size)
    q = QuantumRegister(2*size + 2)
    #b = ClassicalRegister(2*size)

    circuit = QuantumCircuit(control, q)

    # preparing control qubits
    for i in range(2*size):
        circuit.h(control[i])

    # preparing controlled qubits to state 1
    circuit.h(q[0])

    # applying the U_a gates
    for i in range(2*size):
        circuit.append(c_U_a_gate(size, a**2**i, N), [control[2*size-i-1]] + q[:])

    # applying inverse qft
    circuit.append(QFT(num_qubits=2*size, approximation_degree=0, do_swaps=True, inverse=True, insert_barriers=False,
                       name='iqft'), control)
    return circuit

#print(control_qubits(4,7,15))