import logging

import qiskit
from mqt.bench import get_benchmark, utils

from iccore.serialization import read_json


logger = logging.getLogger(__name__)


class QuantumCircuitCache:
    def __init__(self):
        self.circuits = {}
        self.supported_circuits = []
        self.mqt_namespace = "mqtbench"

    def load_mqt_benchmark(self):
        self.supported_circuits = utils.get_supported_benchmarks()

        mqtbench_config_path = utils.get_default_config_path()
        logger.info("Loading MQT benchmark config from: %s", mqtbench_config_path)

        content = read_json(mqtbench_config_path)
        self.circuits = content["benchmarks"]

    def basic_circuit(
        self, num_qubits: int, depth_multiplier: int = 1
    ) -> qiskit.QuantumCircuit:
        """
        Creates a trivial circuit
        """
        qc = qiskit.QuantumCircuit(num_qubits)
        for _ in range(depth_multiplier):
            for idx in range(num_qubits):
                qc.h(idx)
            for idx in range(num_qubits - 1):
                qc.cx(idx, idx + 1)
        qc.measure_all()
        return qc

    def get_circuit(self, label: str, num_qubits: int):
        if label == "sample":
            return self.basic_circuit(num_qubits)
        if label.startswith("sample:") and len(label.strip()) > len("sample:"):
            return self.basic_circuit(num_qubits, int(label.split(":")[1]))
        elif label.startswith(f"{self.mqt_namespace}:"):
            mqt_label = label[len(self.mqt_namespace) + 1 :]
            if not self.circuits:
                self.load_mqt_benchmark()

            self.check_valid(mqt_label, num_qubits)
            return get_benchmark(
                benchmark_name=mqt_label,
                level=1,
                compiler="qiskit",
                circuit_size=num_qubits,
            )

    def check_valid(self, label: str, num_qubits):
        """
        Checks if the given mqt circuit is one of the available benchmarks
        and that it is valid for the given number of qubits
        """

        if label not in self.supported_circuits:
            msg = f"Circuit {label} not in cache."
            raise RuntimeError(msg)

        # Some circuits have subtypes which causes, take the first one found
        name = label.split("-")[0]
        for circuit in self.circuits:
            if circuit["name"] == name:
                working_circuit = circuit
                break

        min_q = working_circuit["min_qubits"]
        max_q = working_circuit["max_qubits"]
        if min_q <= num_qubits <= max_q:
            return
        else:
            msg = (
                f"Circuit {label} not available with {num_qubits} qubits."
                f"Needs {min_q} to {max_q} qubits."
            )
            raise RuntimeError(msg)
