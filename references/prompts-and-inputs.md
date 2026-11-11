# Interactive Prompts and User Input

Use `rich.prompt` to collect interactive input from users in terminal sessions while preserving styling and validation.

## 1. Text Prompt

Collect strings with default values and styling:

```python
from rich.prompt import Prompt

# Basic prompt with default
username = Prompt.ask("Enter username", default="admin", console=console)

# Styled prompt with required non-empty input
project = Prompt.ask(
    "[bold cyan]Project name[/bold cyan]",
    default="my-cli",
    console=console,
)
```

## 2. Constrained Choices

Restrict input to a list of allowed values:

```python
env = Prompt.ask(
    "Deployment target",
    choices=["development", "staging", "production"],
    default="development",
    case_sensitive=False,
    console=console,
)
```

Rich automatically validates user input against the choices, re-prompting with an error message if an invalid value is entered.

## 3. Confirmations (Yes/No)

Ask binary questions:

```python
from rich.prompt import Confirm

if Confirm.ask("Proceed with deployment?", default=True, console=console):
    console.print("[success]Deploying…[/success]")
else:
    console.print("[warning]Aborted by user.[/warning]")
    raise SystemExit(1)
```

## 4. Typed Numeric Prompts

Enforce integers or floats:

```python
from rich.prompt import IntPrompt, FloatPrompt

port = IntPrompt.ask("Listen port", default=8080, console=console)
rate = FloatPrompt.ask("Sample rate", default=0.05, console=console)
```

## 5. Password & Secret Input

Hide input characters for credentials, tokens, or private keys:

```python
api_key = Prompt.ask(
    "[accent]API Token[/accent]",
    password=True,
    console=console,
)
```

Never print the collected secret back to the terminal or logs.

## 6. Non-Interactive Fallbacks & Guardrails

Interactive prompts will fail or block indefinitely in CI/CD, cron jobs, or redirected stdin (`sys.stdin.isatty() is False`). Always guard prompts:

```python
import sys

def get_target_environment(cli_flag: str | None) -> str:
    if cli_flag:
        return cli_flag
    if not sys.stdin.isatty():
        return "development"  # Non-interactive default or fail explicitly
    return Prompt.ask("Target environment", choices=["dev", "prod"], default="dev")
```
