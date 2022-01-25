import numpy as np


def a2jmodN(a, j, N):
    """Compute a^{2^j} (mod N) by repeated squaring, preventing overflows"""
    for i in range(j):
        a = np.mod(a ** 2, N)
    return a
