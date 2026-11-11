# Rich components and API selection

Use this as a focused API map. Confirm exact signatures against the Rich version already installed in the project.

## Console and themes

Create one application-level console. Keep stdout and stderr separate when the command supports machine-readable output.

```python
from rich.console import Console
from rich.theme import Theme

theme = Theme({
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "info": "cyan",
    "muted": "dim",
    "accent": "bold bright_magenta",
})

console = Console(theme=theme)
error_console = Console(stderr=True, theme=theme)
```

Do not set `force_terminal=True` in normal application code. Let Rich detect terminal capability. Use `no_color=True` only when an explicit no-color mode is selected.

## Core renderables

| Component | Use it for |
|---|---|
| `Panel` | A cohesive summary, warning, or grouped section |
| `Table` | Structured rows and columns |
| `Rule` | Major section separators |
| `Columns` | Compact side-by-side renderables |
| `Group` | Grouping multiple renderables into one display |
| `Tree` | Hierarchical data such as directories or attack paths |
| `Layout` | Responsive screen partitioning (header, body, sidebar, footer) |
| `Prompt` / `Confirm` | Interactive user input with validation and defaults |
| `Syntax` | Source code with syntax highlighting |
| `Traceback` | Readable, formatted stack traces with frame suppression |
| `Markdown` | Render Markdown in a terminal |
| `Pretty` / `inspect` | Object introspection and structure formatting |
| `Text` | Fine-grained spans, styling, and markup-safe text |

Example:

```python
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

table = Table(title="Findings", expand=True)
table.add_column("Severity", no_wrap=True)
table.add_column("Finding", ratio=2)
table.add_column("Status", justify="right")

table.add_row(
    Text("HIGH", style="bold red"),
    "Unauthenticated endpoint disclosure",
    "[warning]Needs review[/warning]",
)

console.print(Panel(table, title="[accent]Assessment summary[/accent]"))
```

## Tables

- Use `expand=True` when the table should occupy available width; otherwise let it size naturally.
- Use `ratio` to allocate flexible width between descriptive columns.
- Use `no_wrap=True` only for short values such as IDs, severity, and status.
- Use `overflow="fold"` for descriptions that must remain readable; use `ellipsis` for secondary text.
- Right-align numeric columns.
- Add a table caption or explicit empty-state text when no records exist.
- Avoid very wide tables. Prefer a concise default view and an optional verbose/details view.

## Progress columns

Common columns:

- `SpinnerColumn`
- `TextColumn`
- `BarColumn`
- `TaskProgressColumn`
- `MofNCompleteColumn`
- `TimeElapsedColumn`
- `TimeRemainingColumn`
- `DownloadColumn`
- `TransferSpeedColumn`
- `FileSizeColumn`

Build a reusable `Progress` factory if multiple commands share the same style. Use only columns whose values are meaningful for the task.

## Logging

Use `rich.logging.RichHandler` with the standard `logging` module when possible. Configure it once at the CLI boundary. Avoid configuring handlers from imported library modules.

## Windows and UTF-8 terminal compatibility

On Windows systems (PowerShell / Command Prompt), ensure UTF-8 encoding is enabled to avoid `UnicodeEncodeError`:

```python
import sys

# Ensure UTF-8 output encoding for terminals
if sys.platform == "win32" and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
```

Rich natively handles Windows console color (VT100) via colorama integration. Avoid manual ANSI sequences.

## Dependency policy

Rich is the core dependency. Typer, Click, Questionary, Loguru, and PyFiglet are optional. Do not add them merely for decoration; use the project's existing CLI and logging stack.
