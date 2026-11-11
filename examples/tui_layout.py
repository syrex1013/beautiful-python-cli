#!/usr/bin/env python3
"""Demonstration of a multi-pane Terminal Layout (TUI) with responsive panes."""

from __future__ import annotations

import argparse
import sys
import time

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

THEME = Theme(
    {
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "info": "cyan",
        "muted": "dim",
        "accent": "bold magenta",
    }
)

console = Console(theme=THEME)


def make_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="sidebar", ratio=1),
        Layout(name="content", ratio=2),
    )
    return layout


def render_sidebar(iteration: int) -> Panel:
    table = Table.grid(padding=(0, 1))
    table.add_column(style="muted")
    table.add_column(justify="right")
    table.add_row("Uptime:", f"{iteration * 0.5:.1f}s")
    table.add_row("Memory:", "42.8 MB")
    table.add_row("Active Tasks:", "[accent]4[/accent]")
    table.add_row("Queue Depth:", "[info]12[/info]")
    table.add_row("Health:", "[success]OPTIMAL[/success]")
    return Panel(table, title="[bold]System Status[/bold]", border_style="cyan")


def render_content(iteration: int) -> Panel:
    table = Table(expand=True, box=None)
    table.add_column("Event ID", style="muted", no_wrap=True)
    table.add_column("Source")
    table.add_column("Level")
    table.add_column("Message")

    events = [
        ("EVT-101", "ingest-service", "[success]INFO[/success]", "Payload batch parsed successfully"),
        ("EVT-102", "auth-gateway", "[success]INFO[/success]", "TLS handshake verified with mutual cert"),
        ("EVT-103", "worker-pool", "[warning]WARN[/warning]", "Memory buffer above 70% threshold"),
        ("EVT-104", "storage-node", "[success]INFO[/success]", f"Snapshot #{iteration} committed to disk"),
    ]
    for eid, src, lvl, msg in events:
        table.add_row(eid, src, lvl, msg)

    return Panel(table, title="[bold]Real-Time Stream[/bold]", border_style="magenta")


def main() -> None:
    parser = argparse.ArgumentParser(description="Demonstrate Rich Layout TUI.")
    parser.add_argument("--seconds", type=float, default=2.0, help="Duration to run demonstration")
    args = parser.parse_args()

    layout = make_layout()
    layout["header"].update(
        Align.center("[accent]─── CLUSTER SURVEILLANCE & TELEMETRY TUI ───[/accent]")
    )
    layout["footer"].update(
        Align.center("[muted]Press Ctrl+C to disconnect • Live stream frequency: 2 Hz[/muted]")
    )

    if not console.is_terminal:
        layout["sidebar"].update(render_sidebar(1))
        layout["content"].update(render_content(1))
        console.print(layout)
        return

    with Live(layout, console=console, screen=False, refresh_per_second=4) as live:
        start = time.time()
        iteration = 0
        try:
            while time.time() - start < args.seconds:
                iteration += 1
                layout["sidebar"].update(render_sidebar(iteration))
                layout["content"].update(render_content(iteration))
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass

    console.print("[success]TUI session terminated cleanly.[/success]")


if __name__ == "__main__":
    main()
