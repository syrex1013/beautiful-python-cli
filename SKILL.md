---
name: beautiful-python-cli
description: Design, implement, or refactor Python command-line output into polished, accessible terminal UIs using Rich. Use when adding spinners, loading states, progress bars, concurrent tasks, interactive prompts, live dashboards, TUI layouts, real-time logs, colored status, tables, panels, themes, or terminal UX. Do not use for GUI/web interfaces or trivial one-off scripts that only need plain output.
---

# Beautiful Python CLI

Build terminal interfaces that are useful first and visually polished second. Prefer clear information hierarchy, truthful status, restrained color, and reusable rendering code over decoration.

## Instruction priority

Follow the user's explicit requirements and the repository's established conventions first. This skill supplies defaults where the user or project has not specified a choice. Do not migrate CLI frameworks, redesign unrelated code, or add dependencies without a concrete reason.

## Workflow

1. **Inspect before changing**
   - Read the relevant entry point, CLI framework, `pyproject.toml`/requirements, supported Python version, and nearby tests.
   - Identify whether stdout is intended for humans, scripts, or both.
   - Preserve existing commands, flags, exit codes, output contracts, and business logic.
2. **Choose the smallest useful design**
   - Use `rich` for rendering. Keep the project's existing `argparse`, Typer, Click, or other CLI framework; Typer is optional, not a requirement.
   - Avoid adding `questionary`, `loguru`, or other dependencies when Rich or the existing stack is sufficient.
   - If Rich is missing, explain the dependency and add it through the repository's existing dependency mechanism. Do not silently run a global `pip install`.
3. **Centralize presentation**
   - Create one shared `Console` (or a small UI module) and a reusable semantic theme.
   - Keep UI/rendering separate from domain logic. Prefer functions such as `render_summary`, `render_findings_table`, `show_status`, and `make_progress`.
   - Use stable style names (`success`, `warning`, `error`, `info`, `muted`, `accent`) instead of scattering raw ANSI escapes or color literals.
4. **Match the indicator to the work**
   - Use a spinner/status for work whose completion percentage is unknown.
   - Use a progress bar only when real progress can be measured (items, bytes, stages, or completed tasks).
   - Use a live dashboard only when continuously changing information materially helps the operator.
   - Never invent percentages, ETAs, throughput, completion counts, or scan results.
5. **Handle every output environment**
   - Detect TTY/terminal capability; do not force ANSI color or animation by default.
   - Support `NO_COLOR`, redirected output, CI logs, SSH terminals, and narrow terminal widths.
   - Keep machine-readable output (especially JSON) clean. Send human diagnostics/progress to stderr when stdout is a data stream.
   - Provide a plain or no-color mode when appropriate.
6. **Verify the result**
   - Run focused tests and the project's formatter/linter/type checker where available.
   - Test a normal terminal, redirected/non-TTY output, narrow width, errors, and empty results.
   - Confirm that progress and live displays stop cleanly on success, failure, and cancellation.

## Visual system

Use a restrained, consistent palette with semantic meaning:

| Role | Suggested style | Meaning |
|---|---|---|
| Success | `green` / `bold green` | Completed, valid, healthy |
| Warning | `yellow` / `bold yellow` | Degraded, partial, needs attention |
| Error | `red` / `bold red` | Failed, invalid, blocked |
| Info | `cyan` | Neutral operational information |
| Accent | `bright_magenta` or `bright_blue` | Product identity or emphasis |
| Muted | `dim` | Secondary metadata |

Color must never be the only signal. Pair it with words (`OK`, `WARN`, `FAIL`), symbols, or explicit columns. Avoid rainbow output, excessive bolding, and large banners on every command. Respect user-specified brand colors and existing themes.

## Required UI patterns

### Startup and command header
- Show a compact application name/version only when it adds context.
- Keep banners short; avoid delaying useful output with decorative animations.
- Display target, scope, configuration, or execution mode only when relevant and safe to disclose.
- Never print credentials, tokens, cookies, private keys, or other secrets.

### Spinners and loading states
- Use `console.status("Connecting…", spinner="dots")` for a short, indeterminate operation.
- Choose a spinner that renders reliably in common terminals; allow Rich to fall back when Unicode is unavailable.
- Use `console.status` as a context manager so it stops on exceptions.
- Do not show a spinner for instant operations or when output is non-interactive.
- For multiple independent tasks, prefer a multi-task `Progress` display over nested spinners.

### Progress bars
- Use `rich.progress.Progress` with columns that answer useful questions:
  - `SpinnerColumn` or `TextColumn` for task identity
  - `BarColumn` for visual completion
  - `TaskProgressColumn` or `MofNCompleteColumn` for actual progress
  - `TimeElapsedColumn` and `TimeRemainingColumn` only when meaningful
  - `DownloadColumn` and `TransferSpeedColumn` for byte transfers
- Track real units: files, hosts, requests, records, bytes, or completed stages.
- For unknown totals, use an indeterminate task; do not display a fabricated total.
- For concurrent work, use separate named tasks and synchronized updates. Avoid interleaved `print()` calls from workers.
- Use `transient=True` only when the progress display should disappear after completion; keep important final results visible.
- Disable animated progress when `not console.is_terminal`.

### Tables
- Use `rich.table.Table` for structured results. Give columns concise names and meaningful alignment.
- Right-align numbers; left-align names and descriptions; use `no_wrap` selectively.
- Use sensible overflow (`fold`, `ellipsis`, or `crop`) and let Rich adapt to terminal width.
- Include a useful empty-state message instead of rendering a blank table.
- Sort or group results when that improves scanning; do not hide important fields just to make the table look tidy.
- For security findings, distinguish severity, confidence, status, and evidence; do not imply severity from color alone.

### Panels, summaries, and hierarchy
- Use `Panel` for a cohesive summary, alert, or grouped section—not around every line.
- Use `Rule` for major section boundaries and `Columns`/`Group` for compact related content.
- Put the most actionable information first. Keep secondary metadata dim and concise.
- Prefer one strong summary panel plus detailed tables over many nested boxes.

### Live output and dashboards
- Use `Live` with `Layout`, `Table`, `Group`, or a custom renderable for dashboards that update repeatedly.
- Keep refresh rates modest (typically 4–10 updates/second); slower is usually sufficient for CLI monitoring.
- Use `screen=True` only for intentional full-screen terminal applications. Prefer `screen=False` for ordinary CLI progress.
- Use `console.log()` for timestamped messages while a live display is active; do not call built-in `print()` and corrupt the live region.
- Keep the dashboard readable at narrow widths and provide a final static summary when it exits.
- Ensure `Live` is stopped via a context manager, including on exceptions and Ctrl-C.

### Interactive prompts and user input
- Use `Prompt.ask` for text input with defaults and validation.
- Use `Prompt.ask(..., choices=[...])` for constrained choices instead of freeform parsing.
- Use `Confirm.ask` for yes/no decisions.
- Use `Prompt.ask(..., password=True)` for secrets and tokens; never echo secrets back to stdout.
- Check `sys.stdin.isatty()` and provide safe non-interactive defaults for CI/CD or automated pipelines.

### Tracebacks and error diagnostics
- Use `rich.traceback.install(show_locals=False, max_frames=5)` at the CLI boundary for readable error reports.
- Suppress framework frames (`click`, `typer`, `asyncio`) to focus on user code.
- Only enable `show_locals=True` when explicitly requested via `--debug` or `--verbose`.
- Prefer actionable summary panels for anticipated errors over raw stack traces.

### Layouts and multi-pane TUIs
- Use `rich.layout.Layout` to partition terminal windows into headers, sidebars, main bodies, and footers.
- Combine with `rich.live.Live` for real-time monitoring and surveillance TUIs.
- Default to `screen=False` so command history remains accessible in scrollback.
- Design responsive layouts that remain clean down to 80x24 terminal dimensions.

### Logs and errors
- Use `RichHandler` when integrating Python `logging`; configure it once at the application boundary.
- Keep logs concise and structured. Use timestamps/levels when they help diagnosis, not as decoration.
- Present expected operational errors as short actionable messages; expose tracebacks only in debug mode.
- Preserve non-zero exit codes and send diagnostics to stderr.
- Never swallow exceptions merely to keep the interface attractive.

### Themes and output modes
- Define a `Theme` once and pass it to the shared `Console`.
- Use `Console(no_color=True)` or an explicit `--no-color` option when the project supports it; otherwise rely on terminal detection and `NO_COLOR`.
- When supporting `--json`, `--quiet`, or `--plain`, make these modes real contracts:
  - `--json`: valid JSON only on stdout; no banner, spinner, table, or progress text on stdout.
  - `--quiet`: suppress decorative and routine output while preserving errors and requested machine output.
  - `--plain`: readable text without box drawing or ANSI styling.
- Do not hardcode terminal width. Use Rich's layout/wrapping behavior and test narrow widths.

## Code quality rules

- Prefer Rich renderables over hand-built ANSI escape sequences.
- Use `console.print`, `console.log`, `console.status`, `Progress`, `Live`, `Table`, `Panel`, `Columns`, `Tree`, `Syntax`, and `JSON` where they fit.
- Avoid global monkey-patching, shelling out to `clear`, and repeated terminal erasure.
- Do not couple core operations to Rich objects; return data from core logic and render it at the CLI boundary.
- Do not add decorative output that makes copy/paste, piping, or log parsing harder.
- Use context managers for progress, status, live displays, and other resources.
- Make cancellation and failure paths as polished and reliable as the success path.

## Definition of done

- The output communicates state, progress, results, and errors accurately.
- Spinners are used only for indeterminate work; progress bars reflect real measurements.
- Tables and panels remain readable at typical and narrow terminal widths.
- Live updates do not corrupt logs or final output.
- Redirected, CI, `NO_COLOR`, and JSON output remain usable.
- Existing CLI behavior and exit semantics are preserved.
- Tests or a reproducible manual verification cover the relevant output paths.

## Supporting references

Read only the reference needed for the task:
- `references/rich-components.md` — Rich APIs, columns, tables, themes, and renderables.
- `references/interaction-patterns.md` — spinners, progress, live dashboards, async/concurrency patterns.
- `references/prompts-and-inputs.md` — interactive prompts, validation, secrets, and non-TTY guards.
- `references/tracebacks-and-debugging.md` — exception formatting, syntax highlighting, and introspection.
- `references/layouts-and-tui.md` — multi-pane screen partitioning and dynamic TUIs.
- `references/concurrent-progress.md` — thread-safe and async multi-task progress bars.
- `references/testing-and-accessibility.md` — TTY behavior, JSON/plain output, accessibility, and tests.
- `references/activation-tests.md` — positive and negative prompts for checking skill routing.
- `examples/showcase.py` — comprehensive panels, tables, and progress showcase.
- `examples/live_dashboard.py` — dynamic Live dashboard updating in real-time.
- `examples/interactive_prompts.py` — prompts, input validation, confirmation, and secret masking.
- `examples/concurrent_progress.py` — multi-threaded background workers with simultaneous progress bars.
- `examples/tui_layout.py` — multi-pane terminal layout for system monitoring.
