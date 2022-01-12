# This file contains tests that will be run on github. These tests are also runnable locally using pytest

import sys
sys.path.append(".")

import pytest
import math
from src.quantum.qi_runner import setup_QI, execute_circuit, print_results
from src.quantum.gates.adder_gate import adder, adder_optimized, adder_reduced, parse_num
from src.quantum.gates.modular_adder_gate import modular_adder
from src.quantum.gates.controlled_multiplier_gate import swap_reg, controlled_multiplier_gate, c_swap_register

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

    adder = adder_reduced(num1, size)
    circuit.append(adder, q)

    circuit.append(QFT(num_qubits=size, approximation_degree=0, do_swaps=True, inverse=True, insert_barriers=False, name='iqft'), q)

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

def assert_modular_adder(num1, num2, N):
    size = len((bin(N))) - 1
    q = QuantumRegister(size+3)
    c = ClassicalRegister(size+3)
    circuit = QuantumCircuit(q, c)

    circuit.x(q[0])
    circuit.x(q[1])

    # Set number B
    list_num = parse_num(num2, size)[::-1]
    for i in range(len(list_num)):
        if (list_num[i]):
            circuit.x(q[i + 2])

    circuit.append(QFT(num_qubits=size, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), range(2, size + 2))
    mod_adder = modular_adder(num1, N, size)
    circuit.append(mod_adder, range(0, size+3))
    circuit.append(QFT(num_qubits=size, approximation_degree=0, do_swaps=True, inverse=True, insert_barriers=False, name='iqft'), range(2, size + 2))

    print(circuit.draw())

    qi_result = execute_circuit(circuit, 1)
    counts_histogram = qi_result.get_counts(circuit)
    bin_result = counts_histogram.most_frequent()[0 : size + 1]
    print(bin_result)
    result = int(bin_result, 2)
    expected = (num1+num2) if (num1 + num2) < N else (num1 + num2 - N)
    assert result == expected

def test_modular_adder():
    assert_modular_adder(19, 6, 15)
    assert_modular_adder(10, 10, 17)
    assert_modular_adder(1023, 782, 1000)
    # assert_modular_adder(808763, 1312, 604921)


def assert_controlled_swap(initial_state):
    l = len(initial_state)
    assert l > 2 and l % 2 == 1
    size = (l-1)//2
    c = QuantumRegister(1)
    x = QuantumRegister(size)
    b = QuantumRegister(size)
    cl = ClassicalRegister(l)
    circuit = QuantumCircuit(c,x,b,cl)
    for q in range(l):
        if initial_state[q]:
            circuit.x(q)
    circuit.append(c_swap_register(size), range(l))

    print(circuit.draw())

    qi_result = execute_circuit(circuit, 3)
    counts_histogram = qi_result.get_counts(circuit)
    print(counts_histogram.most_frequent())
    bin_result = [int(i) for i in str(counts_histogram.most_frequent())]
    print(bin_result)
    if initial_state[0]:
        expected = [1] + initial_state[1+size:]+ initial_state[1:1+size]
    else:
        expected = expected = initial_state

    print(expected)
    for i in range(l):
        assert expected[i] == bin_result[::-1][i]



def test_controlled_swap():
    assert_controlled_swap([0, 0, 0, 1, 1, 1, 1, 0, 0])
    assert_controlled_swap([0, 0, 1, 1, 1, 1, 1, 0, 0])
    assert_controlled_swap([0, 1, 1, 0, 0])
    assert_controlled_swap([1, 0, 0, 1, 1, 1, 1, 0, 0])
    assert_controlled_swap([1, 0, 1, 1, 1, 1, 1, 0, 0])
    assert_controlled_swap([1, 1, 1, 0, 0])
