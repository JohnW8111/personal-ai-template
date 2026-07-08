---
name: skill-builder
description: Create, import, simplify, or update self-contained Personal AI skills that can be used by both Codex and Claude. Use when asked to create a skill, import a Claude skill, canonicalize a workflow, make a skill agent-neutral, or decide what belongs in SKILL.md versus references, scripts, or assets. Candidate import adapted from the prior Claude CreateSkill skill for both Codex and Claude.
---

# Skill Builder

Status: candidate import.

## Purpose

Create practical, self-contained skills for Personal AI. The canonical skill should be readable by both Codex and Claude. Tool-specific details belong in adapters only when necessary.

## Skill Folder Pattern

```text
skill-name/
  SKILL.md
  references/    # optional, loaded only when needed
  scripts/       # optional deterministic helpers
  assets/        # optional templates or static assets
```

## Procedure

1. Identify the repeated workflow or specialized knowledge the skill should capture.
2. Choose a lowercase hyphenated folder name.
3. Write `SKILL.md` with only `name` and `description` frontmatter.
4. Put trigger guidance in the description because agents may see metadata before the body.
5. Keep the body concise: purpose, inputs, procedure, output, verification, and agent notes.
6. For a mature skill, include compact normal, difficult-or-ambiguous, and stop-or-approval examples.
7. Move long examples, rubrics, schemas, or methodology details into `references/`.
8. Move deterministic repeated code into `scripts/`.
9. Avoid duplicate guidance across background, memory, and skill files.
10. Remove old PAI identity references, voice hooks, Claude-only paths, and nonportable assumptions.
11. Note any adapter needs for Codex or Claude separately.

## Import Checklist

- [ ] Skill is self-contained.
- [ ] Frontmatter has `name` and `description`.
- [ ] Description names real triggers.
- [ ] No old assistant identity references.
- [ ] No required voice notification.
- [ ] No hard-coded Claude-only path unless it is clearly marked as legacy source material.
- [ ] Tool-specific instructions are optional or adapter-scoped.
- [ ] Verification expectations are explicit.
- [ ] Mature skills include compact normal, difficult, and stop-or-approval examples.

## Verification

- Read the final `SKILL.md` top to bottom.
- Confirm it can be followed without reading the original Claude skill.
- Confirm Codex and Claude have equivalent paths through the workflow.
- If scripts are included, run or syntax-check representative scripts.

## Agent Notes

- Prefer improving one useful skill over importing many weak ones.
- Do not create a skill for a simple one-command utility unless the workflow has judgment, context, or repeated steps.
- Candidate imports should be usable but can be refined after real use.
