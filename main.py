from src.circuit import apply_check, encode_psi, decode_outputs
from src.backend import backend, basis_set, coupling
from src.utils import print_state
from qiskit import QuantumCircuit, execute, ClassicalRegister
import numpy as np
import os

if not os.path.exists('data/'):
    os.makedirs('data/')

# Define theta range
num_theta = 10
theta = np.linspace(0, np.pi,num_theta,endpoint=False)

# Number of algorithm execution for each theta
num_times = 1

# Number of error-correcting block repetition
num_reps = 8

all_data = []
for tt, theta in enumerate(num_theta):
    print('Angle:', theta)
    print('Correct state:')
    print_state( np.array([(1+np.exp(1j*theta)),  (1+np.exp(1j*theta))])/2 )

    syndromes_list = []
    qc = QuantumCircuit(5)
    encode_psi(qc, theta=theta[tt])

    for ii in range(num_reps):
        apply_check(qc, ii)

    creg = ClassicalRegister(4)
    qc.add_register(creg)

    qc.measure(0, creg[0])
    qc.measure(1, creg[1])
    qc.measure(3, creg[2])
    qc.measure(4, creg[3])

    for nn in num_times:
        job = execute(qc, backend=backend, basis_gates=basis_set, 
            coupling_map=coupling, shots=1024)
        counts = job.result().get_counts()
        occurrences, syndromes = decode_outputs(counts)

        # Apply ml model on results
        error_landscape = 'something processed'
        for ii in occurrences:
            print(ii, occurrences[ii])
        
        # Correct occurrences
        
        # Save results