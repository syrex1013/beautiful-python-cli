#!/usr/bin/env python3
"""A small Live dashboard example with a durable final summary."""

from __future__ import annotations

import argparse
import random
import time
from dataclasses import dataclass

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.theme import Theme

THEME = Theme(
    {
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "muted": "dim",
        "accent": "bold cyan",
    }
)


@dataclass
class Worker:
    name: str
    completed: int = 0
    total: int = 12
    state: str = "RUNNING"


def render(workers: list[Worker]) -> Table:
    table = Table(title="Live worker dashboard", expand=True)
    table.add_column("Worker", style="accent")
    table.add_column("State")
    table.add_column("Completed", justify="right")
    table.add_column("Progress", ratio=1)

    for worker in workers:
        if worker.state == "DONE":
            state = "[success]DONE[/success]"
        else:
            state = "[warning]RUNNING[/warning]"
        table.add_row(
            worker.name,
            state,
            f"{worker.completed}/{worker.total}",
            f"{worker.completed / worker.total:.0%}",
        )
    return table


def main() -> int:
    parser = argparse.ArgumentParser(description="Demonstrate a Rich live dashboard.")
    parser.add_argument("--seconds", type=float, default=4.0)
    args = parser.parse_args()

    console = Console(theme=THEME)
    workers = [Worker("worker-01"), Worker("worker-02"), Worker("worker-03")]

    if not console.is_terminal:
        console.print("Live dashboard disabled: stdout is not an interactive terminal.")
        return 0

    deadline = time.monotonic() + max(0.2, args.seconds)
    with Live(render(workers), console=console, refresh_per_second=4, screen=False) as live:
        while time.monotonic() < deadline and any(w.completed < w.total for w in workers):
            for worker in workers:
                if worker.completed < worker.total and random.random() > 0.35:
                    worker.completed += 1
                    if worker.completed == worker.total:
                        worker.state = "DONE"
            live.update(render(workers), refresh=True)
            time.sleep(0.25)

    console.print(render(workers))
    console.print("[success]Dashboard stopped; final state retained.[/success]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
