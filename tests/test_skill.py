"""Automated test suite for Beautiful Python CLI components and patterns."""

from __future__ import annotations

import io
import unittest

from rich.console import Console
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


class TestBeautifulPythonCLI(unittest.TestCase):
    def setUp(self) -> None:
        self.buffer = io.StringIO()
        self.console = Console(
            file=self.buffer,
            theme=THEME,
            force_terminal=True,
            width=80,
            color_system="standard",
        )

    def test_semantic_styles(self) -> None:
        self.console.print("[success]Operation Succeeded[/success]")
        output = self.buffer.getvalue()
        self.assertIn("Operation Succeeded", output)

    def test_no_color_mode(self) -> None:
        no_color_buffer = io.StringIO()
        no_color_console = Console(
            file=no_color_buffer,
            theme=THEME,
            no_color=True,
            width=80,
        )
        no_color_console.print("[error]Failure Occurred[/error]")
        plain_text = no_color_buffer.getvalue()
        self.assertIn("Failure Occurred", plain_text)
        self.assertNotIn("\x1b[", plain_text)  # No ANSI escapes

    def test_table_rendering(self) -> None:
        table = Table(title="Test Findings")
        table.add_column("Key")
        table.add_column("Value", justify="right")
        table.add_row("Status", "OK")
        table.add_row("Count", "42")

        self.console.print(table)
        output = self.buffer.getvalue()
        self.assertIn("Test Findings", output)
        self.assertIn("Status", output)
        self.assertIn("42", output)

    def test_panel_summary(self) -> None:
        panel = Panel("[accent]Important Notice[/accent]", title="Notice")
        self.console.print(panel)
        output = self.buffer.getvalue()
        self.assertIn("Important Notice", output)
        self.assertIn("Notice", output)


if __name__ == "__main__":
    unittest.main()
