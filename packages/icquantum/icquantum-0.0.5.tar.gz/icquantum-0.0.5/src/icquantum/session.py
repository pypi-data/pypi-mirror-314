import logging
from pathlib import Path

from icsystemutils.monitor import Profiler

import icquantum.simulation
from .circuit_cache import QuantumCircuitCache
from .simulation import QuantumSimulation


logger = logging.getLogger(__name__)


def _run_circuits(circuits: list, backend):
    logger.info("Running %d circuits", len(circuits))
    logger.info("trace: Start run_circuits")
    job = backend.run(circuits)
    result = job.result()
    logger.info("trace: Finish run_circuits")
    return result


def run(
    sim: QuantumSimulation,
    backend,
    circuits: QuantumCircuitCache,
    work_dir: Path,
    profilers: list[Profiler] | None = None,
) -> None:

    logger.info("trace: Start benchmark")
    icquantum.simulation.write(work_dir, sim)

    logger.info("trace: Start load_circuits")
    try:
        qc = circuits.get_circuit(sim.circuit_label, sim.num_qubits)
    except RuntimeError as e:
        logger.error("Failed to load circuits with: %s", e)
        raise e

    qcs = [qc] * sim.num_circuits
    logger.info("trace: Finish load_circuits")

    if profilers:
        for profiler in profilers:
            profiler.start()

    logger.info("trace: Start simulation")
    sim.on_started()

    for _ in range(sim.num_iters):
        result = _run_circuits(qcs, backend)

    sim.on_finished()

    all_results = []
    for r in result.to_dict()["results"]:
        counts = r["data"]["counts"]
        seed = r["seed_simulator"]
        circuit_time = r["time_taken"]
        circuit_results = {
            "counts": counts,
            "seed": seed,
            "circuit_simulation_time": circuit_time,
        }
        all_results.append(circuit_results)
    sim.results = all_results
    icquantum.simulation.write(work_dir, sim)
    logger.info("trace: Finish simulation")

    if profilers:
        for profiler in profilers:
            profiler.stop()

    logger.info("trace: Finish benchmark")
