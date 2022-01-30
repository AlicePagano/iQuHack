from src.circuit import apply_check, encode_psi, decode_outputs
from src.backend import backend, basis_set, coupling
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
num_reps = 20

all_data = []
for tt in range(num_theta):
    print('Counter:', tt, theta[tt])

    syndromes_list = []
    for nn in range(num_times):
        qc = QuantumCircuit(5)
        encode_psi(qc, theta=theta[tt])

        for ii in range(num_reps):
            apply_check(qc, ii)
            #for jj in range(6):
            #    qc.id(0)

        creg = ClassicalRegister(4)
        qc.add_register(creg)

        qc.measure(0, creg[0])
        qc.measure(1, creg[1])
        qc.measure(3, creg[2])
        qc.measure(4, creg[3])

        job = execute(qc, backend=backend, basis_gates=basis_set, coupling_map=coupling, shots=1024)
        counts = job.result().get_counts()
        occurrences, syndromes = decode_outputs(counts)
        for ii in occurrences:
            print(ii, occurrences[ii])
        
        if '1111' in occurrences:
            ones = occurrences['1111']
        else:
            ones = 0
        print( 'angle: ',np.arccos(  (occurrences['0000']-ones)/1024 )  )
        input()
        
        syndromes_list.append(syndromes)
    
    all_data.append({'theta': theta[tt], 'all_syndromes': syndromes_list})

np.save('data/num_reps=8_num_times=20.npy', np.array(all_data) )