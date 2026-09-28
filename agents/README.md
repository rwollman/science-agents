# Agent definitions

Place reusable, versioned agent definitions here. Keep per-run memory, checkpoints, logs, and credentials outside the repository.

## Grant review

- [Grant reviewer](grant-reviewer.md): the coordinating reviewer brief, covering logic and support, writing, and independent reviewer critique.
- [Independent grant reviewer](grant-independent-reviewer.md): the self-contained brief supplied to additional agents for independent summaries and critiques.

To use these portable definitions, give your agent the grant-reviewer brief and the proposal, plus any funding instructions, review criteria, and constraints. For example:

> Use `agents/grant-reviewer.md` to review the attached proposal at all three levels. Run two independent readers using `agents/grant-independent-reviewer.md`, and return a coordinated report with suggested edits. Keep the original proposal unchanged.

The coordinating agent must have access to delegation tools to complete Level 3. Independent readers should receive fresh contexts containing the companion brief, the same proposal version, and the supplied funding criteria, without the coordinating review or other readers' reports. If delegation is unavailable, the coordinator must report that limitation and provide handoff briefs rather than claim independent review occurred. Different models can be used when available and requested or authorized; no provider or model is required.

Reviewer-roster research is optional and runs only when explicitly requested. These Markdown files define behavior; the existing skill installer does not install or register them as runtime-specific custom agents.
