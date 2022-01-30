from src.circuit import apply_check, encode_psi, decode_outputs
from src.backend import backend, basis_set, coupling
from src.utils import print_state
from src.dnn_predict import dnn_predict
from qiskit import QuantumCircuit, execute, ClassicalRegister
import numpy as np
from tensorflow import keras
import os

if not os.path.exists('data/'):
    os.makedirs('data/')

# Load network model
model = keras.models.load_model("dnn_predictor.krs")

# Define theta range
num_theta = 1
thetas = np.linspace(0, np.pi,num_theta,endpoint=False)


# Number of error-correcting block repetition
num_reps = 8

all_data = []
for tt, theta in enumerate(thetas):
    print('Angle:', theta)
    print('Correct state:')
    print_state( np.array([(1+np.exp(1j*theta)),  (1+np.exp(1j*theta))])/2 )

    syndromes_list = []
    qc = QuantumCircuit(5)
    encode_psi(qc, theta=theta)

    for ii in range(num_reps):
        apply_check(qc, ii)

    creg = ClassicalRegister(4)
    qc.add_register(creg)

    qc.measure(0, creg[0])
    qc.measure(1, creg[1])
    qc.measure(3, creg[2])
    qc.measure(4, creg[3])

    job = execute(qc, backend=backend, basis_gates=basis_set, 
        coupling_map=coupling, shots=1024)
    counts = job.result().get_counts()
    occurrences, syndromes = decode_outputs(counts)

    # Apply ml model on results
    for meas_state in syndromes:
        for syndrome, n_occ in syndromes[meas_state]:
            print(syndrome, n_occ)
            error_landscape = model()
    #for ii in occurrences:
    #    print(ii, occurrences[ii])
    
    # Correct occurrences
    
    # Save results