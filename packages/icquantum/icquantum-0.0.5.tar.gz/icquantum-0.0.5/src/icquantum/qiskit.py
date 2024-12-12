import logging

from qiskit_aer import Aer

from icquantum.simulation import QuantumSimulationBackend


logger = logging.getLogger(__name__)


def setup_aer_backend(backend_info: QuantumSimulationBackend):
    logger.info(
        "Creating %s - %s backend", backend_info.library, backend_info.library_backend
    )

    aer_backend = Aer.get_backend(backend_info.library_backend)
    if backend_info.use_gpu:
        aer_backend.set_options(device="GPU")
    if backend_info.seed_simulator:
        aer_backend.set_options(seed_simulator=backend_info.seed_simulator)
    aer_backend.set_options(max_parallel_threads=backend_info.num_cores)
    aer_backend.set_options(max_parallel_experiments=backend_info.num_parallel_exp)
    aer_backend.set_options(max_job_size=None)
    aer_backend.set_options(
        statevector_parallel_threshold=backend_info.parallel_threshold
    )
    return aer_backend
