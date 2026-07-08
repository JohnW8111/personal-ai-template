# Claude Code Skill Adapter Notes

Canonical skills live in `personal-ai/skills/`.

Claude Code can read these skill files as normal Markdown workflow instructions. If a workflow needs to be installed into Claude-specific directories later, keep the canonical version here and make the Claude-specific version a wrapper.

For Claude/Cowork execution details - folder access, the capability map to document skills, scheduled tasks, and artifacts - see `capabilities.md` in this directory. Those are execution notes only and do not change any canonical workflow.

## Adapter Principle

- Canonical workflow: `personal-ai/skills/<skill>/SKILL.md`
- Claude-specific wrapper: only when needed for Claude Code discovery or command conventions.
- Do not let Claude-specific wording become the source of truth unless the canonical skill is updated too.

## Easy Switch

During a Claude Code session, type:

```text
PAI on: <your request>
```

Claude should read `personal-ai/ON.md`, load the assistant context, and use relevant background, memory, or skills for that request. This keeps PAI opt-in rather than global.

`PAI on` always refers to this repository's `personal-ai/` directory. Claude
must read `personal-ai/assistant/` first and must not substitute its separate
legacy `~/.claude/PAI` system. That legacy directory is a read-only migration
source: never write new or updated PAI material there. If the canonical
directory is unavailable, ask where it moved.

## Installed Wrapper

Claude Code discovers the PAI switch through a thin wrapper installed at
`~/.claude/skills/PersonalAI/SKILL.md`. The wrapper contains only:

1. Frontmatter with the trigger phrases (copied verbatim from the canonical
   skill's description; this is what Claude Code's auto-discovery reads).
2. A pointer telling Claude to read and follow the canonical skill at
   `personal-ai/skills/personal-ai/SKILL.md`.

Do not add workflow instructions to the wrapper. When the canonical skill's
trigger phrases change, update the wrapper's frontmatter to match; everything
else stays canonical-only so the two copies cannot drift apart.

## Install Pattern

Any future Claude Code skill or command should follow the same rule:

1. Refer to the canonical skill path.
2. Add only Claude-specific execution details.
3. Avoid changing the purpose, output contract, or verification requirements.
