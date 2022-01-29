from circuit import apply_check, encode_psi, decode_outputs
from backend import backend, basis_set, coupling
from qiskit import QuantumCircuit, execute
import numpy as np
import os

if not os.path.exists('data/'):
    os.makedirs('data/')

# Define theta range
num_theta = 200
theta = np.linspace(0,2*np.pi,num_theta,endpoint=False)

# Number of algorithm execution for each theta
num_times = 20

# Number of error-correcting block repetition
num_reps = 8

all_data = []
for tt in range(num_theta):
    print('Counter:', tt)

    syndromes_list = []
    for nn in range(num_times):
        qc = QuantumCircuit(5)
        encode_psi(qc, theta=theta[tt])

        for ii in range(num_reps):
            apply_check(qc, ii)

        qc.measure_all()

        job = execute(qc, backend=backend, basis_gates=basis_set, coupling_map=coupling, shots=1024)
        counts = job.result().get_counts()
        occurrences, syndromes = decode_outputs(counts)
        syndromes_list.append(syndromes)
    
    all_data.append({'theta': theta[tt], 'all_syndromes': syndromes_list})

np.save('data/num_reps=8_num_times=20.npy', np.array(all_data) )