# This file contains tests that will be run on github. These tests are also runnable locally using pytest

import sys
from fractions import Fraction

from qiskit.visualization import plot_histogram

sys.path.append(".")

import pytest
import math
from src.quantum.qi_runner import setup_QI, execute_circuit, print_results
from src.quantum.gates.adder_gate import adder_reduced, parse_num
from src.quantum.gates.modular_adder_gate import modular_adder
from src.quantum.gates.controlled_multiplier_gate import controlled_multiplier_gate, new_controlled_multiplier_gate
from src.quantum.gates.controlled_swap_gate import swap_reg, c_swap_register
from src.quantum.gates.controlled_U_a_gate import c_U_a_gate
from src.quantum.gates.non_optimised_period_finding import period_finding_routine

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
    # l must equal 2*size+1
    # 2 registers length size that will be swapped and 1 control qubit
    l = len(initial_state)
    assert l > 2 and l % 2 == 1
    size = (l-1)//2
    c = QuantumRegister(1)
    x = QuantumRegister(size)
    b = QuantumRegister(size)
    cl = ClassicalRegister(l)
    circuit = QuantumCircuit(c,x,b,cl)

    # preparing initialization of qubits
    for q in range(l):
        if initial_state[q]:
            circuit.x(q)
    circuit.append(c_swap_register(size), range(l))

    print(circuit.draw())

    qi_result = execute_circuit(circuit, 1)
    counts_histogram = qi_result.get_counts(circuit)
    bin_result = [int(i) for i in str(counts_histogram.most_frequent())]
    print(bin_result)

    # calculating expected result dependent on control qubit
    if initial_state[0]:
        expected = [1] + initial_state[1+size:] + initial_state[1:1+size]
    else:
        expected = expected = initial_state

    print(expected)
    for i in range(l):
        # bin result is in reversed order
        assert expected[i] == bin_result[::-1][i]



def test_controlled_swap():
    assert_controlled_swap([0, 0, 0, 1, 1, 1, 1, 0, 0])
    assert_controlled_swap([0, 0, 1, 1, 1, 1, 1, 0, 0])
    assert_controlled_swap([0, 1, 1, 0, 0])
    assert_controlled_swap([1, 0, 0, 1, 1, 1, 1, 0, 0])
    assert_controlled_swap([1, 0, 1, 1, 1, 1, 1, 0, 0])
    assert_controlled_swap([1, 1, 1, 0, 0])


def assert_controlled_multiplier(c1, b, x, a, N):
    size_x = len(bin(x).lstrip("0b"))
    size_b = len(bin(N).lstrip("0b"))

    c_q = QuantumRegister(1, 'c')
    x_q = QuantumRegister(size_x, 'x')
    b_q = QuantumRegister(size_b, 'b')
    c_mod_add = QuantumRegister(1, 'c_mod_add')
    c_r = ClassicalRegister(2 + size_x + size_b, 'c_r')
    circuit = QuantumCircuit(c_q, x_q, b_q, c_mod_add, c_r)

    if c1:
        circuit.x(c_q[0])

    bin_x = parse_num(x, size_x)[::-1]
    for i in range(len(bin_x)):
        if bin_x[i]:
            circuit.x(x_q[i])

    bin_b = parse_num(b, size_b)[::-1]
    for i in range(len(bin_b)):
        if bin_b[i]:
            circuit.x(b_q[i])

    c_mult_gate = controlled_multiplier_gate(size_x, a, N)

    circuit.append(c_mult_gate.to_instruction(), [c_q[0]] + x_q[0:size_x] + b_q[0:size_b] + [c_mod_add[0]])

    qi_result = execute_circuit(circuit, 1)

    counts_histogram = qi_result.get_counts(circuit)
    bin_result = counts_histogram.most_frequent()[1: size_b + 1]
    print(bin_result)
    result = int(bin_result, 2)

    expected = (b + a * x) % N if c1 else b
    assert result == expected


def test_controlled_multiplier():
    pass
    #assert_controlled_multiplier(True, 4, 2, 3, 10)
    #assert_controlled_multiplier(False, 4, 2, 3, 10)



def assert_new_controlled_multiplier(a, x, b, N):
    maximum = max(max(a, x), max(b, N))
    size = len(bin(maximum)) - 2

    q = QuantumRegister(2*size + 3)
    br = ClassicalRegister(2*size + 3)

    c = QuantumCircuit(q, br)
    cm = new_controlled_multiplier_gate(size, a, N)

    # control qubit
    c.x(q[0])


    bin_x = parse_num(x, size)[::-1]
    for i in range(len(bin_x)):
        if bin_x[i]:
            c.x(q[i + 1])

    bin_b = parse_num(b, size)[::-1]
    for i in range(len(bin_b)):
        if bin_b[i]:
            c.x(q[i + size + 1])


    c.append(cm, range(2*size + 3))
    print(cm.draw())
    print(c.draw())

    qi_result = execute_circuit(c, 1)

    counts_histogram = qi_result.get_counts(c)
    bin_result = counts_histogram.most_frequent()[2: size + 2]
    print(bin_result)
    result = int(bin_result, 2)

    assert result == (b + a * x) % N

def test_new_controlled_multiplier_gate():
    #                               (a *x +b) %N
    assert_new_controlled_multiplier(7, 7, 0, 30)
    assert_new_controlled_multiplier(14, 11, 8, 121)
    assert_new_controlled_multiplier(4, 8, 30, 63)
    assert_new_controlled_multiplier(9, 17, 0, 20)
    #assert_new_controlled_multiplier(36, 24, 132, 576)

def assert_c_U_a_gate(c, a, x, N):
    size = len(bin(N)) - 2
    q = QuantumRegister(2*size + 3)
    br = ClassicalRegister(2*size + 3)

    círcuit = QuantumCircuit(q, br)
    U_a = c_U_a_gate(size, a, N)

    # control qubit
    if c: círcuit.x(q[0])


    bin_x = parse_num(x, size)[::-1]
    for i in range(len(bin_x)):
        if bin_x[i]:
            círcuit.x(q[i + 1])

    círcuit.append(U_a, range(2*size + 3))
    print(U_a.draw())
    print(círcuit.draw())

    qi_result = execute_circuit(círcuit, 1)

    counts_histogram = qi_result.get_counts(círcuit)
    bin_result = counts_histogram.most_frequent()[2 + size: 2*size + 2]
    print(bin_result)
    result = int(bin_result, 2)
    if c: assert result == (a * x) % N
    else: assert result == x

def test_c_U_a_gate():
    assert_c_U_a_gate(True, 7, 7, 30)
    assert_c_U_a_gate(False, 7, 13, 15)
    assert_c_U_a_gate(True, 9, 17, 77)
    assert_c_U_a_gate(True, 9, 17, 76)
    assert_c_U_a_gate(True, 9, 17, 20)

def check_period_finding_subroutine():
    size = len(bin(15)) - 2
    circuit = period_finding_routine(size, 2, 15)
    qi_result = execute_circuit(circuit, 1)
    print_results(qi_result, circuit)
    print(circuit.draw())
    counts_histogram = qi_result.get_counts(circuit)
    # bin_result = counts_histogram.most_frequent()[0:2*size]
    plot_histogram(counts_histogram)
    # print(counts_histogram)
    # print(bin_result)
    # result = int(bin_result, 2)
    # print(Fraction(result/2*size).limit_denominator(2*size))
    # print(result)

def test_check_period_finding_subroutine():
    check_period_finding_subroutine()
