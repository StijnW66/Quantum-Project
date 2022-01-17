from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
import math

# This is the most efficient adder which can add up to 26 bit numbers.
def adder_reduced(num, size):
    size += 1
    qubit_register = QuantumRegister(size)
    circuit = QuantumCircuit(qubit_register)

    list_num = parse_num(num, size)
    print(list_num)

    for i in range(size):
        angle_sum = 0
        for j in range(size - i):
            if (list_num[j + i]):
                angle_sum = (angle_sum + (2*3.14)/2**(j+1))
        circuit.p(angle_sum, qubit_register[i])

    return circuit


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
