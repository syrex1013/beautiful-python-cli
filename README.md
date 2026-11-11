# beautiful-python-cli

A comprehensive agent skill for crafting polished, accessible terminal user interfaces (TUIs) and CLI applications in Python using [Rich](https://github.com/Textualize/rich).

Designed for modern AI coding assistants including Claude Code, Cursor, Gemini / Antigravity, Codex, Windsurf, and Pi.

---

## Capabilities

- **Status & Spinners**: Indeterminate operation indicators with clean context manager lifecycle.
- **Progress Bars**: Measurable multi-task, byte-transfer, and ETA progress bars.
- **Live Dashboards & TUIs**: Real-time updating multi-pane layouts with responsive screen partitioning.
- **Interactive Prompts**: Input validation, defaults, yes/no confirmations, and masked secret entries.
- **Structured Output**: Stylized tables, summary panels, and tree structures with terminal width adaptability.
- **Diagnostics & Tracebacks**: Production-safe stack trace formatting and syntax highlighting.
- **Contract Adherence**: Full compliance with `NO_COLOR`, non-TTY environments, and pure machine-readable `--json` streams.

---

## Installation

### Via `npx skills` (Recommended)

Install directly into your AI coding assistant:

```bash
# Add to current project
npx skills add syrex1013/beautiful-python-cli

# Install globally across all agents
npx skills add syrex1013/beautiful-python-cli -g
```

### Via Shell Installer

Clone and run the universal installer:

```bash
git clone https://github.com/syrex1013/beautiful-python-cli.git
cd beautiful-python-cli

# Install for all supported agents
./install.sh --all

# Or target specific agents
./install.sh --claude
./install.sh --cursor
./install.sh --antigravity
./install.sh --codex
./install.sh --windsurf
```

---

## Directory Structure

```text
beautiful-python-cli/
├── SKILL.md                          # Core agent skill instructions and routing
├── package.json                      # npm / skills.sh package metadata
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies (rich)
├── install.sh                        # Multi-agent installer script
├── references/                       # In-depth architectural guides
│   ├── rich-components.md            # Component selection and theme definitions
│   ├── interaction-patterns.md       # Spinners, progress, and live updates
│   ├── prompts-and-inputs.md         # Interactive prompt validation & secrets
│   ├── tracebacks-and-debugging.md   # Error reporting and syntax highlighting
│   ├── layouts-and-tui.md            # Screen partitioning & responsive grids
│   ├── concurrent-progress.md        # Multi-threaded and async workers
│   └── testing-and-accessibility.md  # Non-TTY handling, JSON purity, test suite
├── examples/                         # Runnable implementation patterns
│   ├── showcase.py                   # Tables, panels, status, and progress
│   ├── live_dashboard.py             # Dynamic Live dashboard
│   ├── interactive_prompts.py        # Prompts, choices, and confirmation
│   ├── concurrent_progress.py        # ThreadPoolExecutor multi-bar progress
│   └── tui_layout.py                 # Multi-pane terminal dashboard
└── tests/
    └── test_skill.py                 # Automated unit tests
```

---

## Running the Examples

```bash
python3 -m pip install -r requirements.txt

# Run the comprehensive showcase
python3 examples/showcase.py

# Run interactive wizard demonstration
python3 examples/interactive_prompts.py --non-interactive

# Run multi-threaded progress demo
python3 examples/concurrent_progress.py --workers 4

# Run real-time monitoring TUI
python3 examples/tui_layout.py --seconds 3
```

---

## License

MIT © syrex1013
