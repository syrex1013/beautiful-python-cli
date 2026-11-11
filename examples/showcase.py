#!/usr/bin/env python3
"""A compact Rich showcase: panels, tables, status, and measurable progress."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
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
        "accent": "bold bright_magenta",
    }
)


def make_console(no_color: bool = False) -> Console:
    return Console(theme=THEME, no_color=no_color)


def render_summary(console: Console) -> None:
    summary = Table.grid(padding=(0, 2))
    summary.add_column(style="muted")
    summary.add_column()
    summary.add_row("Target", "demo.internal")
    summary.add_row("Mode", "read-only demonstration")
    summary.add_row("Result", "[success]COMPLETED[/success]")
    console.print(
        Panel(
            summary,
            title="[accent]Python CLI[/accent]",
            subtitle="[muted]Rich interface showcase[/muted]",
            border_style="cyan",
            expand=False,
        )
    )


def render_results(console: Console) -> None:
    table = Table(title="Example results", expand=True)
    table.add_column("ID", style="muted", no_wrap=True)
    table.add_column("Check", ratio=2)
    table.add_column("Status", no_wrap=True)
    table.add_column("Duration", justify="right", no_wrap=True)

    table.add_row("CHK-001", "Configuration loaded", "[success]PASS[/success]", "0.02s")
    table.add_row("CHK-002", "Dependency check", "[success]PASS[/success]", "0.11s")
    table.add_row("CHK-003", "Optional integration", "[warning]SKIPPED[/warning]", "—")
    console.print(table)


def run_progress(console: Console, count: int) -> None:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
        disable=not console.is_terminal,
    ) as progress:
        task = progress.add_task("Processing demonstration items", total=count)
        for _ in range(count):
            time.sleep(0.08)
            progress.advance(task)


def main() -> int:
    parser = argparse.ArgumentParser(description="Showcase a polished Rich CLI.")
    parser.add_argument("--no-color", action="store_true", help="Disable terminal colors.")
    parser.add_argument("--items", type=int, default=20, help="Number of demo progress items.")
    args = parser.parse_args()

    if args.items < 1:
        parser.error("--items must be at least 1")

    console = make_console(no_color=args.no_color)
    console.print()
    render_summary(console)
    console.print()
    render_results(console)
    console.print()

    if console.is_terminal:
        run_progress(console, args.items)
    else:
        console.print(f"Processing {args.items} demonstration items (progress animation disabled).")

    console.print("\n[success]Demo finished.[/success]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
