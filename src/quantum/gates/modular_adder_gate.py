import sys
sys.path.append(".")

from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library import QFT


from src.quantum.qi_runner import setup_QI, execute_circuit, print_results
from src.quantum.gates.adder_gate import adder_reduced


def modular_adder(a, N, size):
    add_a_ciruit = adder_reduced(a, size)
    add_n_ciruit = adder_reduced(N, size)

    add_a_gate = add_a_ciruit.to_gate(label="add a").control(2)

    qubit_register = QuantumRegister(size + 3)
    circuit = QuantumCircuit(qubit_register)

    circuit.append(add_a_gate, range(0, size + 2))

    sub_n_gate = add_n_ciruit.inverse().to_gate(label="sub N")

    circuit.append(sub_n_gate, range(2, size + 2))

    circuit.append(QFT(num_qubits=size, approximation_degree=0, do_swaps=True, inverse=True, insert_barriers=False, name='iqft'), range(2, size + 2))

    circuit.cnot(qubit_register[size+1], qubit_register[size+2])

    circuit.append(QFT(num_qubits=size, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), range(2, size + 2))

    add_n_gate = add_n_ciruit.to_gate(label="add N").control(1)
    list = range(2, size)
    circuit.append(add_n_gate, list.insert(0, size+1))

    return circuit

c = modular_adder(4, 4, 4)

print(c.draw())