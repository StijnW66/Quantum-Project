import sys
sys.path.append(".")
from src.quantum.qi_runner import setup_QI, execute_circuit, print_results

from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
import math


def adder(circuit):
    qubit_register = circuit.qubits
    size = len(qubit_register)

    # apply the cp gates
    for i in range(int(size/2)):
        for j in range(int(size/2) - i):
            circuit.cp((2*3.14* 1) /2**(j+1), qubit_register[j + i], qubit_register[i + int(size/2)])


# parse a number to binary
def parse_num(num, size):
    list_num = [int(x) for x in bin(num)[2:]]
    while (len(list_num) < size):
        list_num.insert(0, 0)
    return list_num

# To optimize further let num be the number with the least number of bits set to 1
def adder_optimized(circuit, num):
    qubit_register = circuit.qubits
    size = len(qubit_register)

    # parse the number to binary.
    list_num = parse_num(num, size/2)

    # apply the cp gates
    for i in range(int(size/2)):
        for j in range(int(size/2) - i):
            if (list_num[(j+i)]):
                circuit.cp((2*3.14* 1) /2**(j+1), qubit_register[(j+i)], qubit_register[i + int(size/2)])


