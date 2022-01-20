from fractions import Fraction

import numpy as np
from qiskit import Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from quantuminspire.credentials import enable_account

from quantum.gates.one_control_qubit import changed_one_control_qubit, classic_one_control_qubit

enable_account("f87c536e3d720c28cc6fc4cec5e4deaba41e4749")

N = 15
a = 11
size = len(bin(N).lstrip("0b"))
# circuit = changed_one_control_qubit(size, a, N)
circuit = classic_one_control_qubit(size, a, N)

aer_sim = Aer.get_backend('aer_simulator')
# aer_sim.set_options(device='GPU')
t_qc = transpile(circuit, aer_sim)
qobj = assemble(t_qc, shots=1024)
results = aer_sim.run(qobj).result()
counts = results.get_counts()
plot_histogram(counts)

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
    print(r)

np.savetxt('results.txt', rows)
