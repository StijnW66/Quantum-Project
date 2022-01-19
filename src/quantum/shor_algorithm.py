import numpy as np
from math import gcd

import sys
sys.path.append(".")
from fractions import Fraction
from src.quantum.qi_runner import setup_QI, execute_circuit, print_results
from src.quantum.gates.control_qubits import control_qubits

from quantuminspire.credentials import enable_account
from qiskit.circuit.library import QFT
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


qi_backend = None
def setup_QI_for_shor():
    enable_account("f09ca950f54ad514f8de09466aff2dc49cee34a5")
    setup_QI("shor")

def find_period(a, N):
    size = len(bin(N)) - 2

    c = QuantumRegister(2*size)
    q = QuantumRegister(2*size+2)
    clas = ClassicalRegister(2*size)
    circuit = QuantumCircuit(c, q, clas)

    circuit.append(control_qubits(size, a, N), c[:] + q[:])
    circuit.measure(range(2*size), range(2*size))
    for i in range(100):
        print("trying to find r. iteration:", i)
        qi_result = execute_circuit(circuit, 1)

        counts_histogram = qi_result.get_counts(circuit)
        bin_result = counts_histogram.most_frequent()[2 + size: 2 * size + 2]
        decimal = int(bin_result[::-1], 2)
        phase = decimal / (2**(2*size))
        f = Fraction(phase).limit_denominator(N)
        r = f.denominator
        print(decimal, phase, r)
        if r > 2:
            if (a**r)%N == 1:
                return r
    #too many tries
    return 1




def shor_algorithm(N):
    #assert N is int
    assert N > 1

    # Small number check
    if N < 3:
        return 1, N

    # Draw random integer 'a' satisfying:  1 < a < N
    a = np.random.randint(2, N - 1)
    K = gcd(a, N)

    # Check for trivial solution
    if K != 1:
        print("found trivial solution by accident")
        return K, N / K

    print("found a:",a)
    # Setting-up connection to QI to prevent multiple authentication
    global qi_backend
    if qi_backend is None:
        qi_backend = setup_QI_for_shor()

    # Quantum Subroutine: Find Period of f(x) = a ** x mod N == 1
    r = find_period(a, N)

    # Check if a ** (r / 2) is integer
    if r % 2 == 1:
        shor_algorithm(N)

    x = (a ** (r / 2)) % N

    # Check if x + 1 is not multiple of N (as then gcd(x + 1, N) = N, which is not solving the problem)
    if (x + 1) % N == 0:
        shor_algorithm(N)

    # Else return factors of N
    print("factors:", gcd(x + 1, N), gcd(x - 1, N))
    return gcd(x + 1, N), gcd(x - 1, N)

factors = shor_algorithm(15)
print("factors:", factors)