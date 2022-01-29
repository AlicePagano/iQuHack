from circuit import apply_check, encode_psi, decode_outputs
from backend import backend, basis_set, coupling
from qiskit import QuantumCircuit, execute
import numpy as np

num_reps = 5
qc = QuantumCircuit(5)
encode_psi(qc)

for ii in range(num_reps):
    apply_check(qc, ii)

qc.measure_all()

job = execute(qc, backend=backend, basis_gates=basis_set, coupling_map=coupling, shots=1024)


counts = job.result().get_counts()

occurrences, syndromes = decode_outputs(counts)

for key in occurrences:
    print(key, occurrences[key])
    print(key, syndromes[key])
    
np.save('data.npy', syndromes) 