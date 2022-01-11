# This file contains tests that will be run on github. These tests are also runnable locally using pytest

import sys
sys.path.append(".")

import pytest
import math
from src.quantum.qi_runner import setup_QI, execute_circuit, print_results
from src.quantum.quantum_gates import adder, adder_optimized, adder_reduced, parse_num

from quantuminspire.credentials import enable_account
from qiskit.circuit.library import QFT
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

# This method runs once before all tests in this file and sets up the quantuminspire interface.
@pytest.fixture(scope='module', autouse=True)
def setup_QI_before_tests():
    enable_account("2a9f882ef038dcca14b930a393e332eae78ce915")
    setup_QI("Tests")


def assert_add_nums_reduced(num1, num2):
    # Calculate the sum to determine the amount of bits needed.
    sum = num1+num2
    size = len((bin(sum))) - 2 # subtract 2 since string starts with 0b
    print(size)

    # Create the circuit
    q = QuantumRegister(size)
    b = ClassicalRegister(size)
    circuit = QuantumCircuit(q, b)

    list_num = parse_num(num2, size)[::-1]

    for i in range(len(list_num)):
        if (list_num[i]):
            circuit.x(q[i])

    circuit.append(QFT(num_qubits=size, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), q)

    adder_reduced(circuit, num1)

    circuit.append(QFT(num_qubits=size, approximation_degree=0, do_swaps=True, inverse=True, insert_barriers=False, name='qft'), q)

    print(circuit.draw())

    # Execute circuit on quantuminspire and check if the correct  value is obtained.
    qi_result = execute_circuit(circuit, 5)
    counts_histogram = qi_result.get_counts(circuit)
    bin_result = counts_histogram.most_frequent()[0:size]
    result = int(bin_result, 2)
    assert result == num1 + num2


def test_reduced():
    assert_add_nums_reduced(11, 14)
    assert_add_nums_reduced(110, 143)
    assert_add_nums_reduced(99, 19)
    assert_add_nums_reduced(194, 171)
    assert_add_nums_reduced(1, 124)
    assert_add_nums_reduced(0, 162)
    assert_add_nums_reduced(82, 0)
    assert_add_nums_reduced(5254, 2083)

    # this takes 20 minutes...
    #assert_add_nums_reduced(60108863, 108863)


# Below are tests for up to 13 qubits added together

def create_adder_circuit(num1, num2, size, optimize):
    # create quantum circuit to hold value a.
    q = QuantumRegister(int(size))
    b = ClassicalRegister(size*2)
    circuit = QuantumCircuit(q, b)

    # create quantum circuit to hold value b. Which is then fourier transformed.
    qftq = QuantumRegister(int(size))
    qft = QuantumCircuit(qftq)

    # convert the numbers to binary and set the corresponding bits to |1>
    list_num1 = parse_num(num1, size)
    list_num2 = parse_num(num2, size)[::-1]
    for i in range(len(list_num1)):
        if (list_num1[i]):
            circuit.x(q[i])

    for i in range(len(list_num2)):
        if (list_num2[i]):
            qft.x(qftq[i])

    # Add quantum fourier transform to bottom qubits
    qft.append(QFT(num_qubits=int(size), approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), qftq)
    circuit += qft

    # Apply the adder to the circuit
    if (optimize):
        adder_optimized(circuit, num1)
    else:
        adder(circuit)

    # Add inverse quantum fourier transform to bottom qubits
    iqft = QuantumCircuit(qftq)
    iqft.append(QFT(num_qubits=int(size), approximation_degree=0, do_swaps=True, inverse=True, insert_barriers=False, name='iqft'), qftq)
    circuit += iqft

    return circuit

def assert_add_nums(num1, num2, optimize):
    # Calculate the sum to determine the amount of bits needed.
    sum = num1+num2
    size = len((bin(sum))) - 2 # subtract 2 since string starts with 0b

    # Create the circuit.
    circuit = create_adder_circuit(num1, num2, size, optimize)


    # Execute circuit on quantuminspire and check if the correct  value is obtained.
    qi_result = execute_circuit(circuit, 3)
    counts_histogram = qi_result.get_counts(circuit)
    bin_result = counts_histogram.most_frequent()[0:size]
    result = int(bin_result, 2)
    assert result == num1 + num2

def test_adder():
    # any sum should work as long as it takes half of maximum qubits.

    assert_add_nums(11, 14, False)
    assert_add_nums(110, 143, True)
    assert_add_nums(99, 19, False)
    assert_add_nums(194, 171, True)
    assert_add_nums(1, 124, False)
    assert_add_nums(0, 162, True)
    assert_add_nums(82, 0, False)

    # This test takes 8 minutes to run and 91 gates for normal adder,
    # The optimized adder takes 6 minutes and 33 gates
    # assert_add_nums(5254, 2083)
