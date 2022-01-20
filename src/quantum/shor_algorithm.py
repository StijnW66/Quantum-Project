import numpy as np
from math import gcd

import sys

from qiskit import Aer, transpile, assemble

from quantum.gates.one_control_qubit import classic_one_control_qubit

sys.path.append(".")
from fractions import Fraction
from src.quantum.qi_runner import setup_QI, execute_circuit, print_results
from src.quantum.gates.control_qubits import control_qubits

from quantuminspire.credentials import enable_account
from qiskit.circuit.library import QFT
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


qi_backend = None
iter = 0

def setup_QI_for_shor():
    enable_account("f87c536e3d720c28cc6fc4cec5e4deaba41e4749")
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

def find_period_optimal(a, N):
    size = len(bin(N).lstrip("0b"))
    # circuit = changed_one_control_qubit(size, a, N)
    circuit = classic_one_control_qubit(size, a, N)

    aer_sim = Aer.get_backend('aer_simulator')
    # aer_sim.set_options(device='GPU')
    t_qc = transpile(circuit, aer_sim)
    qobj = assemble(t_qc, shots=1024)
    results = aer_sim.run(qobj).result()
    counts = results.get_counts()

    counts = results.get_counts(circuit)

    n_count = 2 * size
    rows, measured_phases = [], []

    for output in counts:
        decimal = int(output[::-1], 2)  # Convert (base 2) string to decimal
        # decimal = int(output, 2)  # Convert (base 2) string to decimal
        phase = decimal / (2 ** n_count)  # Find corresponding eigenvalue
        measured_phases.append(phase)
        # Add these values to the rows in our table:
        rows.append([float("{:.3f}".format(phase)), counts[output], Fraction(phase).limit_denominator(N)])

    # Print the rows in a table
    # sort by count
    def number(r):
        return r[1]

    rows.sort(reverse=True, key=number)
    for r in rows:
        den = r[2].denominator
        if a ** den % N == 1:
            return den




def shor_algorithm(N):
    #assert N is int
    assert N > 1

    global iter

    iter += 1

    print("Shor's Algorithm for " + str(N) +": Attempt " + str(iter))


    # Small number check
    if N < 3:
        return 1, N

    # Draw random integer 'a' satisfying:  1 < a < N
    a = np.random.randint(2, N - 1)
    print("\tChosen a: " + str(a))
    K = gcd(a, N)

    # Check for trivial solution
    if K != 1:
        print("\tFound trivial solution by accident")
        return K, int(N / K)

    # Setting-up connection to QI to prevent multiple authentication
    global qi_backend
    if qi_backend is None:
        qi_backend = setup_QI_for_shor()

    # Quantum Subroutine: Find Period of f(x) = a ** x mod N == 1
    r = find_period_optimal(a, N)
    print("\tFound r: " + str(r))

    # Check if a ** (r / 2) is integer
    if r % 2 == 1:
        print("\tPeriod not even, repeating the algorithm" + str(r))
        shor_algorithm(N)

    x = int((a ** (r / 2)) % N)

    # Check if x + 1 is not multiple of N (as then gcd(x + 1, N) = N, which is not solving the problem)
    if (x + 1) % N == 0:
        shor_algorithm(N)

    # Else return factors of N
    # print("factors:", gcd(x + 1, N), gcd(x - 1, N))
    return gcd(x + 1, N), gcd(x - 1, N)

factors = shor_algorithm(15)
print("Factors found:", factors)
