#!/usr/bin/env python3
"""Demonstration of multi-threaded concurrent workers with Rich progress bars."""

from __future__ import annotations

import argparse
import concurrent.futures
import random
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.theme import Theme

THEME = Theme(
    {
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "info": "cyan",
        "muted": "dim",
        "accent": "bold cyan",
    }
)

console = Console(theme=THEME)


def simulate_worker(progress: Progress, task_id: TaskID, name: str, total_chunks: int) -> tuple[str, bool, int]:
    chunks_done = 0
    for chunk in range(total_chunks):
        time.sleep(random.uniform(0.02, 0.06))
        chunks_done += 1
        progress.advance(task_id, advance=1)
        if chunk == total_chunks // 2:
            progress.update(task_id, description=f"[info]{name}[/info] [muted](halfway)[/muted]")
    progress.update(task_id, description=f"[success]{name}[/success] [muted](done)[/muted]")
    return name, True, chunks_done


def main() -> None:
    parser = argparse.ArgumentParser(description="Demonstrate concurrent multi-task progress.")
    parser.add_argument("--workers", type=int, default=4, help="Number of concurrent workers")
    args = parser.parse_args()

    console.print(
        Panel(
            f"[accent]Concurrent Processing Engine[/accent]\n"
            f"[muted]Dispatching {args.workers} background worker threads...[/muted]",
            border_style="cyan",
        )
    )

    results: list[tuple[str, bool, int]] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            task_map = {}
            for i in range(args.workers):
                worker_name = f"Worker #{i + 1}"
                steps = random.randint(15, 25)
                task_id = progress.add_task(f"[accent]{worker_name}[/accent]", total=steps)
                future = executor.submit(simulate_worker, progress, task_id, worker_name, steps)
                task_map[future] = worker_name

            for future in concurrent.futures.as_completed(task_map):
                results.append(future.result())

    # Final summary table
    table = Table(title="Worker Execution Summary", expand=True)
    table.add_column("Worker", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Processed Chunks", justify="right")

    for name, success, chunks in sorted(results):
        status_text = "[success]COMPLETED[/success]" if success else "[error]FAILED[/error]"
        table.add_row(name, status_text, str(chunks))

    console.print(table)


if __name__ == "__main__":
    main()
