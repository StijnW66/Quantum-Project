from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import QFT, MCMT

from src.quantum.gates.modular_adder_gate import modular_adder


def controlled_multiplier_gate(x_size, b_size, a, N):
    # Although one additional controlling qubit 'c1' is specified for controlled
    # multiplier gate, the 'c2' qubit is to match qubit control of modular adder
    c1 = QuantumRegister(1, 'c')
    x = QuantumRegister(x_size, 'x')
    b = QuantumRegister(b_size, 'b')
    c2 = QuantumRegister(1, 'mod_add_c')

    cr = QuantumCircuit(c1, x, b, c2)

    # Create QFT gate and apply to 'b' qubits
    qft_b = QFT(b_size)
    cr.append(qft_b.to_instruction(), b)

    # Create Modular Adder Gates, set control to c1 and x[i] qubits and add to circuit
    for i in range(x_size):
        temp_a = 2 ** i * a
        temp_modular_adder = modular_adder(temp_a, N, b_size)
        cr.append(temp_modular_adder, [c1[0], x[i]] + b[0:b_size] + [c2[0]])

    # Create QFT^(-1) gate and apply to 'b' qubits
    inv_qft_b = QFT(b_size).inverse()

    cr.append(inv_qft_b.to_instruction(), b)



def swap_reg(size):
    # swaps registers x and b
    x = QuantumRegister(size, 'x')
    b = QuantumRegister(size, 'b')
    circuit = QuantumCircuit(x, b)
    circuit.swap(x, b)
    return circuit


def c_swap_register(size):
    # controlled SWAP of registers x and b
    c = QuantumRegister(1, 'c')
    x = QuantumRegister(size, 'x')
    b = QuantumRegister(size, 'b')

    circuit = QuantumCircuit(c, x, b)

    # Create controlled SWAP gate
    c_swap_gate = swap_reg(size).to_gate(label="SWAP").control(1)
    circuit.append(c_swap_gate, range(2 * size + 1))

    return circuit
