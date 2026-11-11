# Layouts and Terminal User Interfaces (TUIs)

Use `rich.layout.Layout` to partition the terminal screen into responsive grids, sidebars, headers, and footers for dashboards and monitoring tools.

## 1. Basic Layout Hierarchy

```python
from rich.layout import Layout
from rich.panel import Panel

layout = Layout()

# Split into header, body, and footer
layout.split_column(
    Layout(name="header", size=3),
    Layout(name="body", ratio=1),
    Layout(name="footer", size=3),
)

# Split the body into sidebar and main area
layout["body"].split_row(
    Layout(name="sidebar", ratio=1),
    Layout(name="main", ratio=3),
)

# Populate panels
layout["header"].update(Panel("[accent]Monitoring Dashboard[/accent]", style="bold"))
layout["sidebar"].update(Panel("Node Status\n• Node 1: [success]OK[/success]\n• Node 2: [warning]BUSY[/warning]"))
layout["main"].update(Panel("Recent Telemetry Events", border_style="cyan"))
layout["footer"].update(Panel("[muted]Press Ctrl+C to exit | Refresh: 1.0s[/muted]"))

console.print(layout)
```

## 2. Dynamic Live TUI

Combine `Layout` with `rich.live.Live` for continuously updating full-screen or embedded monitoring:

```python
import time
from rich.live import Live

with Live(layout, console=console, screen=False, refresh_per_second=4) as live:
    try:
        while True:
            # Update individual panes without re-creating the layout tree
            layout["main"].update(render_telemetry_table())
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass
```

## 3. Best Practices
- **Use `screen=False` by default**: Leaves scrollback history intact when the command terminates. Only use `screen=True` for full-screen curses-style apps.
- **Set fixed `size` for headers and footers**: Let the body use `ratio=1` to absorb the remaining vertical space.
- **Test at 80x24**: Ensure the layout degrades gracefully in small terminal windows without raising truncation errors.
- **Provide clean exit handling**: Catch `KeyboardInterrupt` cleanly so the terminal state restores properly.
