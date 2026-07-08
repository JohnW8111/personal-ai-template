# Shared Skills

This directory stores canonical, agent-neutral skills.

The skill files should be readable by any capable coding assistant. Tool-specific adapters can be added under `adapters/`, but the canonical workflow should live here once.

## Skill Folder Pattern

```text
skills/
  skill-name/
    SKILL.md
    scripts/       # optional deterministic helpers
    references/    # optional details loaded only when needed
    assets/        # optional templates or static assets
```

## Skill Rules

- Every skill should have a `SKILL.md`.
- Treat each skill as self-contained. The trigger, purpose, workflow, required context, outputs, scripts, references, and examples should live inside that skill folder.
- Keep the skill body concise.
- Put detailed examples or long references in `references/`.
- Put repeatable deterministic work in `scripts/`.
- Avoid tool-specific instructions in the canonical skill unless there is no neutral way to describe the workflow.
- Do not duplicate skill instructions into `assistant/`, `background/`, or `memory/`. Those files can mention that a skill exists, but the skill remains the source of truth.

## Skills

- `setup`: first-run plain-language interview that fills in the user's personal files.
- `personal-ai`: opt into this context for a request or session.
- `weekly-review`: generate the Weekly PAI Review via the deterministic local tool.
- `research`: run quick, standard, or deep source-backed research with evidence ledgers, linked artifacts, and verification gates.
- `extract-wisdom`: extract insight reports from long-form content.
- `thinking`: choose a structured thinking mode for analysis, critique, or ideation.
- `process-forge`: design and improve processes using DMADV, QFD, human factors, and FMEA.
- `parser`: extract structured data and JSON from messy content.
- `skill-builder`: create or import self-contained agent-neutral skills.

Add your own domain skills (briefings, finance, writing, relationships) as
repeated workflows emerge; use `skill-builder` to scaffold them.
