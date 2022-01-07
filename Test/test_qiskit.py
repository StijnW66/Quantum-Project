import sys
sys.path.append(".")

import pytest
import math
from src.src_quantum.qi_runner import setup_QI, execute_circuit

from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


@pytest.fixture(scope='module', autouse=True)
def setup_QI_before_tests():
    setup_QI("Tests")

def test_entagle():
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)

    circuit.h(q[0])
    circuit.cx(q[0], q[1])
    circuit.measure(q, b)

    probabilities, counts = execute_circuit(circuit)

    for state, val in probabilities.items():
        assert math.isclose(val, 0.5, abs_tol=0.05)



def test_double_hadamard():
    q = QuantumRegister(2)
    b = ClassicalRegister(2)
    circuit = QuantumCircuit(q, b)
    circuit.h(q[0])
    circuit.h(q[1])
    circuit.measure(q, b)

    probabilities, counts = execute_circuit(circuit)
    for state, val in probabilities.items():
        assert math.isclose(val, 0.25, abs_tol=0.05)