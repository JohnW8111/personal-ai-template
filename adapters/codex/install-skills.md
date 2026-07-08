# Codex Skill Adapter Notes

Canonical skills live in `personal-ai/skills/`.

Codex can use those files directly when this folder is in the working context. If a skill should become an installed Codex skill later, create a thin copy or generated adapter under `~/.codex/skills/` that points back to the canonical workflow.

## Adapter Principle

- Canonical workflow: `personal-ai/skills/<skill>/SKILL.md`
- Codex-specific wrapper: only when needed for auto-triggering, bundled scripts, or UI metadata.
- Do not edit the Codex wrapper in a way that diverges from the canonical skill without updating the canonical skill first.

## Easy Switch

During a Codex session, type:

```text
PAI on: <your request>
```

Codex should read `personal-ai/ON.md`, load the assistant context, and use relevant background, memory, or skills for that request. This keeps PAI opt-in rather than global.

`PAI on` always refers to this directory. Codex must read `assistant/`
first. If the directory is unavailable, ask where it moved.

## Future Install Pattern

For an installed Codex skill, use:

```text
~/.codex/skills/<skill>/
  SKILL.md
  agents/openai.yaml
  scripts/       # optional, if Codex needs local deterministic helpers
  references/    # optional
```

The installed `SKILL.md` should either mirror the canonical file or clearly state that `personal-ai/skills/<skill>/SKILL.md` is the source of truth.
