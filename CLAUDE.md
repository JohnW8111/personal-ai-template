# CLAUDE.md — Personal AI (PAI) System

This folder is the user's Personal AI (PAI) system. This file exists so that any
Claude session with this folder connected understands what the PAI switch means.

## Important: PAI is opt-in. Do not auto-load it.

Do NOT read or apply the PAI context by default just because this folder is
connected. Work normally unless the user flips the switch.

## When the user flips the switch

If the user says any of these — `PAI on`, `PAI on:`, `Personal AI on`,
`PAI setup`, `PAI remember:`, `PAI feedback:`, `PAI inbox:`, or asks to use
the personal-ai context — read `ON.md` in this folder and follow its
activation contract exactly. `ON.md` is the single source of truth for the
loading order, capture commands, and skill selection; do not re-derive those
steps from this file.

## First-time users

If the user says `PAI setup`, asks to get started, or seems new while the
`assistant/` files still contain template prompts, use
`skills/setup/SKILL.md` — a plain-language interview that fills in their
personal files for them. Assume no technical background.

## PAI skills are workflow files

A PAI "skill" is a workflow file at `skills/<name>/SKILL.md`. To "use a skill,"
READ that file and follow it. Do not look for it in a tool-side skill registry
and do not report it as missing.

## Some skills may read folders outside this one

Skills may reference external data (briefing folders, transcript archives,
document collections). Each skill's `SKILL.md` names its sources. If a source
is not connected or not found, request access or ask where it moved — do not
invent content.

## Parity

Canonical workflows are agent-neutral and shared with other assistants.
Claude-specific execution details live only in `adapters/claude/`. Do not move
Claude-specific instructions into canonical files.
