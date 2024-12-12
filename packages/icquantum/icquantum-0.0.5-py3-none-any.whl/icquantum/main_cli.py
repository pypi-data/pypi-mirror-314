#!/usr/bin/env python3

import argparse
import logging
import sys
import os
from pathlib import Path

from iccore.serialization import read_yaml
from icsystemutils.monitor import Profiler
from icplot.graph import generator, Plot
from icplot.color import Color

import ictasks
from icflow.sweep import reporter

import icquantum.session
from icquantum.simulation import QuantumSimulation, QuantumSimulationBackend
from icquantum.circuit_cache import QuantumCircuitCache
from icquantum import postprocessing


logger = logging.getLogger(__name__)


def setup_logging(trace_log: bool = False):

    if trace_log:
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.INFO,
            format="%(created)0.6f | %(thread)d | %(message)s",
        )
    else:
        t_fmt = "%(asctime)s%(msecs)03d"
        fmt = f"{t_fmt} | %(filename)s:%(lineno)s:%(funcName)s | %(message)s"
        logging.basicConfig(
            format=fmt,
            datefmt="%Y%m%dT%H:%M:%S:",
            level=logging.INFO,
        )


def benchmark(args):

    setup_logging(args.with_trace_log)

    # We need logging set up before qiskit is imported if we want to
    # control the qiskit logger

    logger.info("trace: Start qiskit_import")
    import qiskit  # NOQA

    logging.info("trace: Finish qiskit_import")
    logging.info("trace: Start aer_import")
    from icquantum.qiskit import setup_aer_backend  # NOQA

    logging.info("trace: Finish aer_import")

    qiskit_version = qiskit.version.get_version_info()
    par_thres = args.parallelization_threshold
    backend = QuantumSimulationBackend(
        library="qiskit_aer",
        library_version=qiskit_version,
        num_cores=args.num_cores,
        num_parallel_exp=args.num_parallel_exp,
        parallel_threshold=par_thres,
        use_gpu=args.use_gpu,
        library_backend="statevector_simulator",
        seed_simulator=args.seed_simulator,
    )

    simulation = QuantumSimulation(
        circuit_label=args.circuit,
        num_qubits=args.num_qubits,
        num_iters=args.num_iters,
        num_circuits=args.num_circuits,
        backend=backend,
    )

    qiskit_backend = setup_aer_backend(simulation.backend)

    circuits = QuantumCircuitCache()

    profilers = []
    if args.do_profile:
        profilers.append(Profiler())

    try:
        icquantum.session.run(
            simulation, qiskit_backend, circuits, args.work_dir.resolve(), profilers
        )
    except RuntimeError as e:
        logger.error("Exception while running session: %s", e)
        sys.exit(1)


def postprocess(args):

    setup_logging()

    result_dir = args.result_dir.resolve()
    tasks = ictasks.task.read_all(result_dir)
    if args.config:
        config = read_yaml(args.config.resolve())
        tasks = reporter.filter_tasks_with_config(
            tasks, config, reporter.task_params_in_range
        )
    completed_tasks = [t for t in tasks if t.finished]
    successful_tasks = [t for t in completed_tasks if t.return_code == 0]
    results = [
        icquantum.simulation.read(result_dir / ictasks.task.get_task_dirname(t))
        for t in successful_tasks
    ]

    # This should be read from file
    config = generator.PlotConfig(
        series_attr="circuit_label",
        x_attr="num_qubits",
        plots={
            "runtime": Plot(
                title="Circuit Simulation Time vs. Number of Qubits",
                x_label="Number of Qubits",
                y_label="Runtime (s)",
                legend_label="circuit",
            ),
        },
        colormap={"sample": Color()},
    )

    generator.plot(results, config, postprocessing.get_point, result_dir)


def postprocess_trace(args):

    setup_logging()
    tasks = ictasks.task.read_all(args.result_dir.resolve())
    postprocessing.collect_traces(tasks, args.trace_config.resolve())


def main_cli():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    benchmark_parser = subparsers.add_parser("benchmark")

    benchmark_parser.add_argument(
        "--work_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Directory for writing results to",
    )
    benchmark_parser.add_argument(
        "--num_qubits", type=int, default=5, help="Number of qubits in the circuit"
    )
    benchmark_parser.add_argument(
        "--num_circuits",
        type=int,
        default=1,
        help="Number of copies of the circuit to send to the backend",
    )
    benchmark_parser.add_argument(
        "--num_iters",
        type=int,
        default=1,
        help="Number of times to repeat the analysis",
    )
    benchmark_parser.add_argument(
        "--num_cores",
        type=int,
        default=0,
        help="Number of cores to use, default of 0 uses all available cores",
    )
    benchmark_parser.add_argument(
        "--num_parallel_exp",
        type=int,
        default=1,
        help="Number of experiments to run in parallel in qiskit",
    )
    benchmark_parser.add_argument(
        "--parallelization_threshold",
        type=int,
        default=14,
        help=("Number of Qubits at which to parallelise" " individual circuits"),
    )
    benchmark_parser.add_argument(
        "--profile",
        action="store_true",
        dest="do_profile",
        default=False,
        help="Enables profiling with cProfile",
    )
    benchmark_parser.add_argument(
        "--use_gpu",
        action="store_true",
        dest="use_gpu",
        default=False,
        help="Enables GPU acceleration",
    )
    benchmark_parser.add_argument(
        "--circuit",
        type=str,
        default="sample",
        help="Pick a circuit from mqtbench using this label",
    )
    benchmark_parser.add_argument(
        "--seed_simulator",
        type=int,
        default=None,
        help="Seed the backend simulator. This will give identical repeats of an "
        "entire batch of circuits, NOT identical results for each circuit.",
    )
    benchmark_parser.add_argument(
        "--with_trace_log",
        action="store_true",
        default=False,
        help="If this flag is included use a higher resolution logger",
    )
    benchmark_parser.set_defaults(func=benchmark)

    benchmarkpp_parser = subparsers.add_parser("benchmark_postprocess")
    benchmarkpp_parser.add_argument(
        "--result_dir",
        type=Path,
        required=True,
        help="The path to directory to be searched.",
    )
    benchmarkpp_parser.add_argument(
        "--config",
        type=Path,
        default="",
        help="The config to specify data to be postprocessed.",
    )

    benchmarkpp_parser.set_defaults(func=postprocess)

    tracepp_parser = subparsers.add_parser("trace_postprocess")
    tracepp_parser.add_argument(
        "--result_dir",
        type=Path,
        required=True,
        help="The path to directory to be searched.",
    )
    tracepp_parser.add_argument(
        "--trace_config",
        type=Path,
        required=True,
        help="Path to the configuration for the trace output.",
    )
    tracepp_parser.set_defaults(func=postprocess_trace)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
