import numpy as np
from math import gcd
from qi_runner import setup_QI

qi_backend = None


def find_period(a, N, qi_backend):
    return 1


def shor_algorithm(N):
    assert N is int
    assert N > 1

    # Small number check
    if N < 3:
        return 1, N

    # Draw random integer 'a' satisfying:  1 < a < N
    a = np.randomint(2, N - 1)
    K = gcd(a, N)

    # Check for trivial solution
    if K != 1:
        return K, N / K

    # Setting-up connection to QI to prevent multiple authentication
    global qi_backend
    if qi_backend is None:
        qi_backend = setup_QI()

    # Quantum Subroutine: Find Period of f(x) = a ** x mod N == 1
    r = find_period(a, N, qi_backend)

    # Check if a ** (r / 2) is integer
    if r % 2 == 1:
        shor_algorithm(N)

    x = (a ** (r / 2)) % N

    # Check if x + 1 is not multiple of N (as then gcd(x + 1, N) = N, which is not solving the problem)
    if (x + 1) % N == 0:
        shor_algorithm(N)

    # Else return factors of N
    return gcd(x + 1, N), gcd(x - 1, N)