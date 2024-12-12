from pathlib import Path
from typing import Any

from icsystemutils.monitor import tracing


def collect_traces(tasks, trace_config_path: Path):

    for task in tasks:
        task_dir = task.get_taskdir()
        trace_file = task_dir / "task_stdout.txt"

        events = tracing.process(trace_file, trace_config_path)
        print(events)


def get_point(result: Any, x_attr: str, y_attr: str) -> tuple[float, float]:
    """
    Return a point (x, y) on a plot series given attributes of the
    result for the xaxis and yaxis
    """
    xval = float(getattr(result, x_attr))
    if y_attr == "runtime":
        return xval, (result.end_time - result.start_time)
    raise RuntimeError(f"Requested yattr '{y_attr}' not recognized")
