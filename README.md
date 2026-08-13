# science-agents

Portable infrastructure for reusable scientific-agent skills.

This repository intentionally separates reusable definitions from runtime state:

- `skills/` contains portable Agent Skills, each rooted at `SKILL.md`.
- `agents/` is reserved for reusable project-level agent definitions.
- `scripts/`, `install/`, `docs/`, `tests/`, and `examples/` support the reusable infrastructure.
- Run state, caches, notebook sessions, outputs, and credentials belong outside the repository.

The initial science skills are placeholders only; substantive scientific procedures will be added after the infrastructure is established.

## Install skills

Run `./install/install.sh` to link the skills into `${AGENTS_HOME:-$HOME/.agents}/skills`. Override the destination with `SCIENCE_AGENTS_SKILLS_HOME`.

## Validate

Run `python3 tests/test_layout.py`.

## Persistent Jupyter

Live-kernel support is maintained as the separate `persistent_jupyter` component and is not vendored into this repository.
