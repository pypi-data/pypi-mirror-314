import time
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from iccore.serialization.json_utils import write_model, read_json


class QuantumSimulationBackend(BaseModel):

    num_cores: int = 1
    num_parallel_exp: int = 0
    parallel_threshold: int = 14
    library: str = ""
    library_version: str = ""
    use_gpu: bool = False
    library_backend: str = ""
    seed_simulator: Any = None


class QuantumSimulation(BaseModel):

    results: list[dict] = []
    state: str = "created"
    start_time: float = 0
    end_time: float = 0
    circuit_label: str = "sample"
    num_circuits: int = 1
    num_qubits: int = 1
    num_iters: int = 1
    backend: QuantumSimulationBackend = QuantumSimulationBackend()

    def on_started(self):
        self.start_time = time.time()
        self.state = "started"

    def on_finished(self):
        self.end_time = time.time()
        self.state = "finished"


def write(
    directory: Path,
    simulation: QuantumSimulation,
    filename: str = "quantum_simulation.json",
):
    write_model(simulation, directory / filename)


def read(
    directory: Path, filename: str = "quantum_simulation.json"
) -> QuantumSimulation:
    return QuantumSimulation(**read_json(directory / filename))
