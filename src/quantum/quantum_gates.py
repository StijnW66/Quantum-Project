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


