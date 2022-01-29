from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import numpy as np

def encode_psi(circ, theta=0):
    """Encode the logical state |psi(theta)> on a quantum circuit qc,
    where |psi> = 0.5*( (1+e^{i\theta})|0> + (1-e^{i\theta})|1> )
    

    Parameters
    ----------
    circ : QuantumCircuit
        qiskit quantum circuit
    theta : float
        Angle of rotation along z
    """
    creg = ClassicalRegister(1, 'initialization')
    circ.add_register(creg)
    for ii in range(5):
        circ.reset(ii)

    circ.h(2)
    circ.rz(theta)
    circ.h(2)
    for ii in range(5):
        if ii==2:
            continue
        circ.cx(2, ii)

    circ.h(2)
    circ.cz(0, 2)
    circ.measure(2, creg[0])
    circ.barrier()

def apply_check(circ, check_num):
    """Apply a check on the quantum circuit

    Parameters
    ----------
    circ : qc
        qiskit quantum circuit
    check_num : int
        Number of the check
    """
    if not isinstance(circ, QuantumCircuit):
        raise TypeError()

    creg = ClassicalRegister(2, f'check{check_num}')

    permutations = np.array([0, 1, 3, 4])
    idx = check_num%4
    ctrls = np.roll(permutations, idx)

    circ.add_register(creg)
    
    circ.cx(ctrls[0], 2)
    circ.cx(ctrls[1], 2)
    circ.measure(2, creg[0])
    
    circ.cx(ctrls[1], 2)
    circ.cx(ctrls[2], 2)
    circ.measure(2, creg[1])

