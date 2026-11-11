#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="beautiful-python-cli"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

INSTALL_OMP=0
INSTALL_PI=0
INSTALL_CODEX=0
INSTALL_CLAUDE=0
INSTALL_CURSOR=0
INSTALL_ANTIGRAVITY=0
INSTALL_WINDSURF=0
EXPLICIT_SELECTION=0

usage() {
  cat <<'EOF'
Install the Beautiful Python CLI skill for AI coding agents.

Usage:
  ./install.sh --all
  ./install.sh --claude
  ./install.sh --cursor
  ./install.sh --antigravity
  ./install.sh --codex
  ./install.sh --windsurf
  ./install.sh --pi
  ./install.sh --omp

Targets:
  Claude Code   ~/.claude/skills/
  Cursor        ~/.cursor/skills/
  Antigravity   ~/.gemini/antigravity-cli/skills/
  Codex         ~/.agents/skills/
  Windsurf      ~/.codeium/windsurf/skills/
  Pi            ~/.pi/agent/skills/
  OMP           ~/.omp/agent/skills/

With no target flags, --all is used.
Existing installations are backed up before replacement.
EOF
}

for arg in "$@"; do
  case "$arg" in
    --all)
      EXPLICIT_SELECTION=1
      INSTALL_OMP=1
      INSTALL_PI=1
      INSTALL_CODEX=1
      INSTALL_CLAUDE=1
      INSTALL_CURSOR=1
      INSTALL_ANTIGRAVITY=1
      INSTALL_WINDSURF=1
      ;;
    --omp)
      EXPLICIT_SELECTION=1
      INSTALL_OMP=1
      ;;
    --pi)
      EXPLICIT_SELECTION=1
      INSTALL_PI=1
      ;;
    --codex)
      EXPLICIT_SELECTION=1
      INSTALL_CODEX=1
      ;;
    --claude)
      EXPLICIT_SELECTION=1
      INSTALL_CLAUDE=1
      ;;
    --cursor)
      EXPLICIT_SELECTION=1
      INSTALL_CURSOR=1
      ;;
    --antigravity|--gemini)
      EXPLICIT_SELECTION=1
      INSTALL_ANTIGRAVITY=1
      ;;
    --windsurf)
      EXPLICIT_SELECTION=1
      INSTALL_WINDSURF=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n\n' "$arg" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ "$EXPLICIT_SELECTION" -eq 0 ]]; then
  INSTALL_OMP=1
  INSTALL_PI=1
  INSTALL_CODEX=1
  INSTALL_CLAUDE=1
  INSTALL_CURSOR=1
  INSTALL_ANTIGRAVITY=1
  INSTALL_WINDSURF=1
fi

install_to() {
  local parent="$1"
  local destination="${parent}/${SKILL_NAME}"
  local temporary="${parent}/.${SKILL_NAME}.tmp.$$"
  local backup=""

  mkdir -p "$parent"
  rm -rf "$temporary"
  mkdir -p "$temporary"
  cp -R "${SOURCE_DIR}/." "$temporary/"

  if [[ -e "$destination" ]]; then
    backup="${destination}.backup.$(date +%Y%m%d-%H%M%S)-$$"
    mv "$destination" "$backup"
  fi

  if ! mv "$temporary" "$destination"; then
    if [[ -n "$backup" && -e "$backup" ]]; then
      mv "$backup" "$destination"
    fi
    printf 'Failed to install into %s\n' "$destination" >&2
    return 1
  fi

  printf 'Installed: %s\n' "$destination"
  if [[ -n "$backup" ]]; then
    printf 'Previous copy backed up: %s\n' "$backup"
  fi
}

if [[ "$INSTALL_CLAUDE" -eq 1 ]]; then
  install_to "${HOME}/.claude/skills"
fi
if [[ "$INSTALL_CURSOR" -eq 1 ]]; then
  install_to "${HOME}/.cursor/skills"
fi
if [[ "$INSTALL_ANTIGRAVITY" -eq 1 ]]; then
  install_to "${HOME}/.gemini/antigravity-cli/skills"
fi
if [[ "$INSTALL_CODEX" -eq 1 ]]; then
  install_to "${HOME}/.agents/skills"
fi
if [[ "$INSTALL_WINDSURF" -eq 1 ]]; then
  install_to "${HOME}/.codeium/windsurf/skills"
fi
if [[ "$INSTALL_PI" -eq 1 ]]; then
  install_to "${HOME}/.pi/agent/skills"
fi
if [[ "$INSTALL_OMP" -eq 1 ]]; then
  install_to "${HOME}/.omp/agent/skills"
fi

printf '\nDone. Start a new agent session if the skill is not discovered automatically.\n'
