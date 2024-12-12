import shutil

from iccore.test_utils import get_test_output_dir

import icquantum.session
from icquantum.simulation import QuantumSimulation
from icquantum.circuit_cache import QuantumCircuitCache
from icquantum.qiskit import setup_aer_backend


def test_benchmarking():

    work_dir = get_test_output_dir()

    simulation = QuantumSimulation()
    simulation.circuit_label = "sample"
    simulation.num_qubits = 5
    simulation.num_iters = 3
    simulation.num_circuits = 10
    simulation.backend.library = "qiskit_aer"
    simulation.backend.library_version = "1.2.3"
    simulation.backend.num_cores = 0
    simulation.backend.library_backend = "statevector_simulator"

    qiskit_backend = setup_aer_backend(simulation.backend)
    circuits = QuantumCircuitCache()

    icquantum.session.run(simulation, qiskit_backend, circuits, work_dir)
 
    shutil.rmtree(work_dir)

