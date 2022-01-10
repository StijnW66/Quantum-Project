import sys
sys.path.append(".")
from src.quantum.qi_runner import setup_QI, execute_circuit, print_results


from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
import math


def adder(circuit):
    qubit_register = circuit.qubits
    size = len(qubit_register)

    for i in range(int(size/2)):
        for j in range(int(size/2) - i):
            circuit.cp((2*3.14* 1) /2**(j+1), qubit_register[j + i], qubit_register[i + int(size/2)])


# Some code here to quickly test it out
q = QuantumRegister(8)
b = ClassicalRegister(8)
circuit = QuantumCircuit(q, b)

circuit.x(q[0])
circuit.x(q[4])

for i in range(8):
    circuit.h(q[i])

adder(circuit)

for i in range(8):
    circuit.h(q[i])

print(circuit.draw())

setup_QI(project_name="Adder test")

qi_result = execute_circuit(circuit)

print_results(qi_result, circuit)