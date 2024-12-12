"""
This module allows reporting on past or current parameter sweeps.
"""

import logging
import csv
from typing import Callable
from pathlib import Path

import ictasks
from ictasks.task import Task
from icsystemutils.monitor.sample import Sample
from icplot.graph import Plot, matplotlib, LinePlotSeries, PlotAxis, Range, Color

logger = logging.getLogger()


def deserialize_args(cli_args: str, delimiter: str = "--") -> dict[str, str]:
    """
    Convert command line args in the form 'program --key0 value0 --key1 value1'
    to a dict of key value pairs.
    """
    stripped_entries = [e.strip() for e in cli_args]
    args: dict = {}
    last_key = ""
    for entry in stripped_entries:
        if entry.startswith(delimiter):
            if last_key:
                # Flag
                args[last_key] = ""
            last_key = entry[len(delimiter) :]
        else:
            if last_key:
                args[last_key] = entry
                last_key = ""
    return args


def task_params_in_range(task: Task, config: dict[str, dict]) -> bool:
    """
    Check that this task's parameters are in line with the upper and lower bounds
    and specific values given in the config.
    """

    for key, value in deserialize_args(task.launch_cmd).items():
        if key not in config:
            continue
        param = config[key]

        if "range" in param:
            value_range = param["range"]
            if "lower" in value_range:
                if value < param["lower"]:
                    return False
            if "upper" in value_range:
                if value > param["upper"]:
                    return False
        if "values" in param:
            values = param["values"]
            if "exclude" in values:
                if value in values["exclude"]:
                    return False
            if "include" in values:
                if value not in values["include"]:
                    return False
    return True


def filter_tasks_with_config(
    tasks: list[Task], config: dict, predicate: Callable
) -> list[Task]:
    return [t for t in tasks if predicate(t, config)]


def get_task_times(tasks_dir: Path):
    tasks = ictasks.task.read_all(tasks_dir)

    time_points: list[dict] = []
    for task in tasks:
        for event in "launch", "finish":
            time_points.append(get_time_point(task, event))
    sorted_time_points = sorted(time_points, key=lambda d: d["time"])

    task_timelines: dict[float, int] = {}
    current_n_tasks = 0
    for time_point in sorted_time_points:
        if time_point["event"] == "launch":
            current_n_tasks += 1
        else:
            current_n_tasks -= 1
        task_timelines[time_point["time"]] = current_n_tasks
    return task_timelines


def get_time_point(task, event_type) -> dict[str, float | str]:
    time_point: dict[str, float | str] = {}
    time_point["event"] = event_type
    if event_type == "launch":
        time_point["time"] = task.launch_time
    else:
        time_point["time"] = task.finish_time
    return time_point


def monitor_plot(sweep_dir: Path):

    monitor_dir = sweep_dir / "monitor"
    tasks_dir = sweep_dir / "tasks"

    with open(monitor_dir / "monitor.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        samples = [Sample(**dict(row)) for row in reader]

    task_lifetimes = get_task_times(tasks_dir)

    task_times = list(task_lifetimes.keys())
    n_tasks = list(task_lifetimes.values())

    sample_times = [s.sample_time for s in samples]
    cpu_percent = [s.cpu_percent for s in samples]

    # Normalize times
    min_time = min(task_times[0], sample_times[0])
    task_times = [t - min_time for t in task_times]
    monitor_times = [t - min_time for t in sample_times]

    monitor_series = LinePlotSeries(
        x=monitor_times, y=cpu_percent, label="cpu", marker=""
    )
    task_series = LinePlotSeries(
        x=task_times,
        y=n_tasks,
        label="tasks",
        position_right=True,
        drawstyle="steps-post",
        marker="",
        highlight=True,
        color=Color(),
    )

    monitor_plt = Plot(
        title="CPU usage and concurrent tasks during the sweep against time.",
        x_axis=PlotAxis(label="Time (s)"),
        y_axes=[
            PlotAxis(
                label="CPU usage (Percent)",
            ),
            PlotAxis(
                label="Number of running tasks",
                ticks=Range(lower=0, upper=max(n_tasks) + 1, step=1),
            ),
        ],
        series=[monitor_series, task_series],
        legend="none",
    )

    matplotlib.render(monitor_plt, monitor_dir / "monitor.svg")
