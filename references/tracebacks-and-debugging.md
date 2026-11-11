# Tracebacks, Syntax, and Introspection

Use Rich's diagnostics to make errors actionable and debugging intuitive without leaking internal implementation details to end users.

## 1. Polished Tracebacks

Install Rich's traceback handler at the application boundary (entry point):

```python
from rich.traceback import install

# Production mode: concise, syntax-highlighted tracebacks with suppressed internal frames
install(
    show_locals=False,
    max_frames=5,
    suppress=["click", "typer", "urllib3", "requests"],
)

# Debug mode (--debug / --verbose): include local variable values for troubleshooting
if debug_mode:
    install(show_locals=True, max_frames=20)
```

### Guidelines
- In production, keep `show_locals=False` to prevent leaking sensitive variables (tokens, passwords, PII) in stack dumps.
- Suppress framework frames (`click`, `typer`, `asyncio`) to direct attention to user-authored code.
- For expected operational errors (e.g. file not found, bad network connection), print a concise error panel instead of dumping a full stack trace:

```python
try:
    connect_to_server(host)
except ConnectionError as err:
    error_console.print(
        Panel(
            f"[error]Could not connect to {host}:[/error] {err}\n"
            "[muted]Check your network connection or verify --host.[/muted]",
            title="[error]Connection Failed[/error]",
            border_style="red",
        )
    )
    raise SystemExit(1)
```

## 2. Syntax Highlighting

Render snippets of Python, JSON, YAML, or SQL directly in the terminal:

```python
from rich.syntax import Syntax

code_snippet = """def hello(name: str) -> str:
    return f"Hello, {name}!"
"""

syntax = Syntax(
    code_snippet,
    lexer="python",
    theme="monokai",
    line_numbers=True,
    word_wrap=True,
)
console.print(syntax)
```

## 3. Object Introspection with `inspect`

Debug complex objects, types, or modules interactively:

```python
from rich import inspect

# Inspect attributes and methods
inspect(my_object, methods=True)

# Inspect with docstrings and help
inspect(my_object, help=True)
```

## 4. Pretty-Printing Structures

Format complex dictionaries, lists, or dataclasses without messy `pprint`:

```python
from rich.pretty import pprint

data = {"user": "alice", "roles": ["admin", "developer"], "active": True}
pprint(data, indent_guides=True, expand_all=False)
```
