from circuit import apply_check, encode_0
from backend import backend, basis_set, coupling
from qiskit import QuantumCircuit, execute


num_reps = 5
qc = QuantumCircuit(5)
encode_0(qc)

for ii in range(num_reps):
    apply_check(qc, ii)

qc.measure_all()

job = execute(qc, backend=backend, basis_gates=basis_set, coupling_map=coupling, shots=1024)


counts = job.result().get_counts()
occurrences = {}
error_path = {}
for key in counts:
    results = key.split(' ')
    
    if results[0] in occurrences:
        occurrences[ results[0]] += counts[key]
        error_path[ results[0]].append( results[1:-1][::-1] )
    else:
        occurrences[ results[0]] = counts[key]
        error_path[ results[0]] = [ results[1:-1][::-1] ]

for key in occurrences:
    print(key, occurrences[key])
    print(key, error_path[key])
    