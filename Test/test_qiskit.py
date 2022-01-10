# This file contains tests that will be run on github. These tests are also runnable locally using pytest

import sys
sys.path.append(".")

import pytest
import math
from src.quantum.qi_runner import setup_QI, execute_circuit, print_results
from src.quantum.quantum_gates import adder

from quantuminspire.credentials import enable_account
from qiskit.circuit.library import QFT
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

# This method runs once before all tests in this file and sets up the quantuminspire interface.
@pytest.fixture(scope='module', autouse=True)
def setup_QI_before_tests():
    enable_account("2a9f882ef038dcca14b930a393e332eae78ce915")
    setup_QI("Tests")

# Simple test that uses quantuminspire to entangle two qubits.
def test_entagle():
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)

    circuit.h(q[0])
    circuit.cx(q[0], q[1])
    circuit.measure(q, b)

    probabilities = execute_circuit(circuit).get_probabilities(circuit)

    for state, val in probabilities.items():
        assert math.isclose(val, 0.5, abs_tol=0.1)


def parse_numbers(num1, num2, size):
    # convert numbers to binary and put in a list.
    list_num1 = [int(x) for x in bin(num1)[2:]]
    list_num2 = [int(x) for x in bin(num2)[2:]]

    # pad list with 0's
    while (len(list_num1) < size):
        list_num1.insert(0, 0)
    while (len(list_num2) < size):
        list_num2.insert(0, 0)

    # reverse the second list. Due to the fourier transforms do_swaps the second number is swapped twice (which is okay),
    # but the first number is only swapped once. However since the lists are used in reverse order later on we need to reverse the 2nd list to correct.
    list_num2 = list_num2[::-1]
    print(list_num1)
    print(list_num2)
    return list_num1, list_num2


def create_adder_circuit(num1, num2, size):
    # create quantum circuit to hold value a.
    q = QuantumRegister(int(size))
    b = ClassicalRegister(size*2)
    circuit = QuantumCircuit(q, b)

    # create quantum circuit to hold value b. Which is then fourier transformed.
    qftq = QuantumRegister(int(size))
    qft = QuantumCircuit(qftq)

    # convert the numbers to binary and set the corresponding bits to |1>
    list_num1, list_num2 = parse_numbers(num1, num2, size)
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
    adder(circuit)

    # Add inverse quantum fourier transform to bottom qubits
    iqft = QuantumCircuit(qftq)
    iqft.append(QFT(num_qubits=int(size), approximation_degree=0, do_swaps=True, inverse=True, insert_barriers=False, name='iqft'), qftq)
    circuit += iqft

    # print(circuit.draw())
    return circuit

def assert_add_nums(num1, num2):
    # Calculate the sum to determine the amount of bits needed.
    sum = num1+num2
    size = len((bin(sum))) - 2 # subtract 2 since string starts with 0b

    # Create the circuit.
    circuit = create_adder_circuit(num1, num2, size)

    # Execute circuit on quantuminspire and check if the correct  value is obtained.
    qi_result = execute_circuit(circuit, 3)
    counts_histogram = qi_result.get_counts(circuit)
    bin_result = counts_histogram.most_frequent()[0:size]
    result = int(bin_result, 2)
    assert result == num1 + num2

def test_adder():
    # any sum should work as long as it takes half of maximum qubits.

    assert_add_nums(11, 14)
    assert_add_nums(110, 143)
    assert_add_nums(99, 19)
    assert_add_nums(194, 171)
    assert_add_nums(1, 124)
    assert_add_nums(0, 162)
    assert_add_nums(82, 0)

    # This test takes 8 minutes to run.
    #assert_add_nums(5254, 2083)

