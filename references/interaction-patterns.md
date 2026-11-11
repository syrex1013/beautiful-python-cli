# Interaction patterns: loading, progress, and live output

## 1. Indeterminate operation: spinner

Use when duration is unknown and there is no honest measurable denominator.

```python
with console.status("[info]Connecting to service…[/info]", spinner="dots"):
    client.connect()
```

The context manager stops the spinner even if the operation raises. Keep the message action-oriented and update it when the phase changes.

## 2. Measurable operation: progress bar

```python
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
    console=console,
    transient=False,
    disable=not console.is_terminal,
) as progress:
    task = progress.add_task("Processing files", total=len(files))
    for path in files:
        process(path)
        progress.advance(task)
```

Use `total=None` only when the total is genuinely unknown. Do not estimate progress by elapsed time unless the task is explicitly time-based and the estimate is clearly labeled.

## 3. Multiple tasks

Use one `Progress` object with a task per independently progressing operation. Give each task a stable, concise description. Keep a separate final summary after the context manager exits.

For worker threads or async tasks, route progress events through a shared coordinator or lock if updates can race. Do not let workers write arbitrary text directly into the terminal.

## 4. Download/transfer progress

For transfers, prefer `DownloadColumn`, `TransferSpeedColumn`, and `FileSizeColumn`. Update completed bytes from actual transfer callbacks. Do not display an ETA until there is enough observed throughput to make it meaningful.

## 5. Live dashboard

```python
from rich.live import Live
from rich.table import Table

def build_dashboard(snapshot):
    table = Table(title="Worker status", expand=True)
    table.add_column("Worker")
    table.add_column("State")
    table.add_column("Completed", justify="right")
    for worker in snapshot:
        table.add_row(worker.name, worker.state, str(worker.completed))
    return table

with Live(
    build_dashboard(initial_snapshot),
    console=console,
    refresh_per_second=4,
    screen=False,
) as live:
    while running:
        snapshot = read_current_state()
        live.update(build_dashboard(snapshot), refresh=True)
```

Use a dashboard only when live state helps the operator make decisions. Keep the refresh rate modest. Use `screen=True` only for a deliberately full-screen TUI, and ensure keyboard/cancellation behavior is designed accordingly.

While a `Live` display is active, use `console.log()` for log messages so Rich can preserve the live region. Do not mix in built-in `print()` calls.

## 6. Async tasks

Use the project's existing async architecture. Update progress after awaited work completes, not when it is merely scheduled. Cancel child tasks cleanly and close the progress/live context in `finally` or with context managers.

## 7. Stage-based work

For operations with named phases but no measurable subtask counts, show a concise stage indicator or spinner message:
- `1/4 Validate configuration`
- `2/4 Connect`
- `3/4 Execute`
- `4/4 Summarize`

Only use `N/M` when the number and order of stages are fixed and real.

## 8. Final state

After loading/progress ends, show a durable summary:
- outcome (success, partial, failed, cancelled)
- actual completed/failed counts
- elapsed time if measured
- output paths or next action
- concise warnings

Do not leave the user with only a completed progress bar and no result.
