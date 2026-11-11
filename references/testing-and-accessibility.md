# Testing, accessibility, and output contracts

## Terminal and redirected output

- Let Rich detect terminal capability; do not force ANSI output by default.
- Disable animated progress when `console.is_terminal` is false.
- Respect `NO_COLOR` and explicit `--no-color`.
- Test SSH, CI, redirected stdout, and narrow terminal widths.
- Do not rely on Unicode symbols being available. Use text labels as a fallback.
- Never use color as the only indicator of severity or success.

## stdout, stderr, and JSON

If stdout is a machine-readable stream, keep it free of banners, progress bars, logs, and status messages.

```python
import json
import sys
from rich.console import Console

data_console = Console(file=sys.stdout, no_color=True)
diagnostic_console = Console(file=sys.stderr)

if args.json:
    json.dump(result, sys.stdout)
    sys.stdout.write("\n")
else:
    render_human_result(data_console, result)
```

Send progress and diagnostics to stderr when stdout is reserved for JSON, CSV, or another pipeable format. Keep `--quiet`, `--plain`, and `--json` behavior documented and tested.

## Narrow widths

- Avoid hardcoded terminal widths in normal rendering.
- Use flexible table columns and wrapping.
- Test at widths such as 40, 60, 80, and 120 columns.
- Keep essential identifiers visible; wrap or truncate only secondary descriptions.

## Snapshot and unit testing

Rich supports an in-memory console:

```python
from io import StringIO
from rich.console import Console

buffer = StringIO()
test_console = Console(
    file=buffer,
    force_terminal=True,
    width=80,
    record=True,
)
test_console.print("[success]Completed[/success]")

plain_text = test_console.export_text(styles=False)
assert "Completed" in plain_text
```

Test semantic content, not brittle ANSI escape sequences. Add tests for:
- empty result sets
- success and failure states
- exceptions and Ctrl-C/cancellation
- `--no-color` / `NO_COLOR`
- non-TTY and redirected output
- JSON purity
- narrow terminal widths
- progress completion and cleanup

For deterministic snapshots, fix time values and avoid asserting spinner animation frames.

## UX checklist

- Can a user identify the current operation immediately?
- Is the difference between unknown progress and measurable progress clear?
- Are success, warning, and failure distinguishable without color?
- Are tables readable when the terminal is narrow?
- Can users copy results without decorative noise?
- Does the application still work when output is piped?
- Does every spinner/live display stop on all exit paths?
