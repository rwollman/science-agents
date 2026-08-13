# Repository guidance

Keep reusable, portable agent behavior under `skills/` and reusable agent definitions under `agents/`.

Do not commit credentials, generated scientific outputs, notebook sessions, caches, checkpoints, or other runtime state. Keep new `SKILL.md` files compatible with the open Agent Skills structure; isolate vendor-specific metadata in optional subdirectories.

The current skills are intentionally minimal placeholders. Add substantive scientific instructions only in a deliberate follow-up change with tests or examples.
