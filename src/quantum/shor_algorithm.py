import numpy as np
import sys

from quantum.period_finding_subroutine.period_finding_subroutine import find_period_2n_plus_3
from math import gcd

sys.path.append(".")

shor_attempt_number = 0
chosen_numbers = set()


def shor_algorithm(N):
    # Assert that passed N is valid a number
    assert type(N) is int, "The given number is not an integer!"
    assert N > 1, "The given number has to be greater than 1"

    # Set global variables and print message to indicate start of the Shor's Algorithm
    global shor_attempt_number
    global chosen_numbers
    shor_attempt_number += 1
    print("Shor's Algorithm for " + str(N) + ": Attempt " + str(shor_attempt_number))

    # Small number check
    if N <= 3:
        print(f"\tThe given number {N} is a prime. Terminating the algorithm.\n")
        return 1, N

    # Check if based on past attempts number is prime. Preventing infinite run
    if len(chosen_numbers) >= N - 2:
        print(f"\t Based on past attempts, it seems that given number {N} is prime. Terminating the algorithm.\n")
        return 1, N

    # Draw random integer 'a' such that:  1 < a < N
    a = np.random.randint(2, N)
    while a in chosen_numbers:
        a = np.random.randint(2, N - 1)
    chosen_numbers.add(a)
    print("\tChosen a: " + str(a))
    K = gcd(a, N)

    # Check for trivial solution
    if K != 1:
        print("\tFound trivial solution as randomly chosen 'a' shares divisor with 'N'")
        return K, int(N / K)

    # Quantum Subroutine: Find Period of f(x) = a ** x mod N == 1
    # Note: The subroutine of shor's algorithm is set up to run locally.
    r = sys.maxsize
    while r == sys.maxsize:
        r = find_period_2n_plus_3(a, N)
    print("\tFound period 'r': " + str(r))

    # Check if a ** (r / 2) is integer
    if r % 2 == 1:
        print("\tPeriod is not even, repeating the algorithm.\n")
        return shor_algorithm(N)
    else:
        print("\tPeriod is even, proceeding with algorithm.")

    # Determine 'middle point' 'x'
    x = int((a ** (r / 2)) % N)

    # Check if x + 1 is not multiple of N (as then gcd(x + 1, N) = N, which is not solving the problem)
    if (x + 1) % N == 0:
        print(f"\t{a}^({int(r / 2)}) mod {N} == -1, repeating the algorithm.\n")
        return shor_algorithm(N)

    # Else return factors of N
    return gcd(x + 1, N), gcd(x - 1, N)
