from qiskit import QuantumRegister, QuantumCircuit


from src.quantum.gates.controlled_multiplier_gate import controlled_multiplier_gate, new_controlled_multiplier_gate
from src.quantum.gates.controlled_swap_gate import c_swap_register


def c_U_a_gate(size, a, N):
    # controlled U_a gate
    c1 = QuantumRegister(1, 'c')
    x = QuantumRegister(size, 'x')
    b = QuantumRegister(size + 1, 'b') # add + 1 to account for overflow.
    c2 = QuantumRegister(1, 'mod_add_c')

    circuit = QuantumCircuit(c1, x, b, c2)

    # adding controlled multiplier gate
    c_mult_a_gate = new_controlled_multiplier_gate(size, a, N)
    circuit.append(c_mult_a_gate, range(2 * size + 3))

    #return circuit
    # adding controlled swap register gate
    c_swap_gate = c_swap_register(size)
    circuit.append(c_swap_gate, range(2 * size + 1))

    # adding inverse controlled multiplier gate
    c_mult_a_inverse_gate = new_controlled_multiplier_gate(size, modinv(a, N), N).inverse()
    circuit.append(c_mult_a_inverse_gate, range(2 * size + 3))

    return circuit



# modular inverse code from https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
#print(c_U_a_gate(6,7,15))