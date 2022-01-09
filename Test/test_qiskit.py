# This file contains tests that will be run on github. These tests are also runnable locally using pytest

import sys
sys.path.append(".")

import pytest
import math
from src.quantum.qi_runner import setup_QI, execute_circuit

from quantuminspire.credentials import enable_account
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


# Simple test that uses quantuminspire to apply two hadamard gates.
def test_double_hadamard():
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)
    circuit.h(q[0])
    circuit.h(q[1])
    circuit.measure(q, b)

    probabilities = execute_circuit(circuit).get_probabilities(circuit)
    for state, val in probabilities.items():
        assert math.isclose(val, 0.25, abs_tol=0.1)