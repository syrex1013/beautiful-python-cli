# Skill routing and quality checks

Use these prompts to evaluate whether the skill is discoverable and stays within its intended scope.

## Prompts that should activate the skill

1. "Make this Python CLI output look professional with Rich panels and tables."
2. "Add a spinner while the API connection is being established."
3. "Show real progress for this file-processing loop, including elapsed time."
4. "Build a live terminal dashboard for my concurrent workers."
5. "Improve the CLI's colors, status indicators, logging, and error messages."
6. "Make this scanner's terminal output readable over SSH and in CI."
7. "Add a clean JSON mode without progress bars contaminating stdout."
8. "Refactor the CLI output into reusable Rich components."

## Prompts that should not activate the skill by default

1. "Build a React dashboard for this Python service." — this is a web UI.
2. "Create a Tkinter desktop application." — this is a GUI.
3. "Explain what a Python generator is." — no CLI presentation work.
4. "Write a one-line Python script that prints hello." — plain output is sufficient.
5. "Optimize this SQL query." — unrelated to terminal UX.

## Review criteria

For an activation test, verify both routing and execution:

- Did the agent inspect the existing CLI and dependency setup first?
- Did it preserve the current CLI framework and output contract?
- Did it select a spinner for unknown progress and a bar only for measurable progress?
- Did it avoid fabricated progress, ETA, or throughput?
- Did it account for TTY, redirected output, JSON, and `NO_COLOR`?
- Did it add only necessary dependencies?
- Did it test errors, empty results, narrow widths, and cleanup?
