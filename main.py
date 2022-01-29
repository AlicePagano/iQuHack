from circuit import apply_check, encode_psi, decode_outputs
from backend import backend, basis_set, coupling
from qiskit import QuantumCircuit, execute
import numpy as np
import os

if not os.path.exists('data/'):
    os.makedirs('data/')

num_reps = 20

theta_range = np.linspace(0,2*np.pi,200,endpoint=False)

for theta in theta_range:

    qc = QuantumCircuit(5)
    encode_psi(qc, theta=theta)

    for ii in range(num_reps):
        apply_check(qc, ii)

    qc.measure_all()

    job = execute(qc, backend=backend, basis_gates=basis_set, coupling_map=coupling, shots=1024)


    counts = job.result().get_counts()

    occurrences, syndromes = decode_outputs(counts)

    #for key in occurrences:
    #    print(key, occurrences[key])
    #    print(key, syndromes[key])
        
    file_name = 'data/theta='+str(np.round(theta,3))+'.npy'
    np.save(file_name, np.array(syndromes)) 