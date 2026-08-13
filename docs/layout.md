# Repository layout

| Path | Purpose |
| --- | --- |
| `skills/` | Portable Agent Skills and their optional resources |
| `agents/` | Reusable project-level agent definitions |
| `scripts/` | Repository maintenance utilities |
| `install/` | Global-skill installation helpers |
| `docs/` | Architecture and usage notes |
| `tests/` | Infrastructure validation |
| `examples/` | Small, versioned usage examples |

Runtime state is deliberately absent. Store it in an external location such as `${XDG_STATE_HOME:-$HOME/.local/state}/science-agents`, or in a project-local ignored directory when isolation is more useful.

`persistent_jupyter` is a sibling repository, not a subtree, submodule, or vendored copy.
