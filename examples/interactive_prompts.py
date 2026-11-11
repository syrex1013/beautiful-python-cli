#!/usr/bin/env python3
"""Demonstration of interactive prompts, validation, and confirmation dialogs."""

from __future__ import annotations

import argparse
import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
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

console = Console(theme=THEME)


def main() -> None:
    parser = argparse.ArgumentParser(description="Demonstrate Rich interactive prompts.")
    parser.add_argument("--non-interactive", action="store_true", help="Run with simulated answers")
    args = parser.parse_args()

    console.print(
        Panel(
            "[accent]CLI Configuration Wizard[/accent]\n"
            "[muted]Demonstrates Prompt, Confirm, IntPrompt, and secret masking.[/muted]",
            border_style="magenta",
        )
    )

    if args.non_interactive or not sys.stdin.isatty():
        console.print("[info]Running in non-interactive mode. Using defaults.[/info]")
        project = "my-awesome-app"
        env = "staging"
        port = 8080
        proceed = True
    else:
        project = Prompt.ask("[bold]Project Name[/bold]", default="my-awesome-app", console=console)
        env = Prompt.ask(
            "[bold]Environment[/bold]",
            choices=["development", "staging", "production"],
            default="staging",
            console=console,
        )
        port = IntPrompt.ask("[bold]Service Port[/bold]", default=8080, console=console)
        _token = Prompt.ask("[bold]API Token (masked)[/bold]", password=True, console=console)
        proceed = Confirm.ask("\nSave configuration and initialize?", default=True, console=console)

    if proceed:
        console.print(
            Panel(
                f"[success]Configuration saved![/success]\n\n"
                f"• Project: [accent]{project}[/accent]\n"
                f"• Environment: [info]{env}[/info]\n"
                f"• Port: [muted]{port}[/muted]",
                title="[success]Summary[/success]",
                border_style="green",
            )
        )
    else:
        console.print("[warning]Setup aborted by user.[/warning]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[error]Operation cancelled.[/error]")
        sys.exit(130)
