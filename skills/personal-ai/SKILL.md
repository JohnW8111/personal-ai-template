---
name: personal-ai
description: Opt into this repository's personal-ai context for a request or session. Use when the user says "PAI on", starts with "PAI on:", uses "PAI remember:", "PAI feedback:", or "PAI inbox:", says "Personal AI on", "use personal-ai", "use my Personal AI context", or asks to work from the personal-ai folder.
---

# Personal AI

## Purpose

Load the user's local Personal AI context only when requested.

## Trigger Phrases

- `PAI on`
- `PAI remember:`
- `PAI feedback:`
- `PAI inbox:`
- `Personal AI on`
- `use personal-ai`
- `use my Personal AI context`
- `use the personal-ai skill`

## Procedure

Read `ON.md` in the folder selected for this session and follow its activation contract exactly. `ON.md`
is the single source of truth for the loading order, the capture commands
(`PAI remember:`, `PAI feedback:`, `PAI inbox:`), substantial-task rules, and
skill selection. Do not restate or re-derive the contract from this file; only
the triggers, resolution rules, output behavior, and examples below live here.

## System Resolution

- `PAI on` resolves to the folder containing `ON.md` in the selected workspace.
- If that folder is unavailable, ask the user where it moved instead of guessing.

## Output Behavior

- Briefly confirm: `PAI context loaded.`
- Do not dump the context back to the user.
- Keep this context active for the rest of the current workspace conversation.
- A new conversation starts without Personal AI context until the user invokes the switch again.
- If the user says `PAI off` or `Personal AI off`, stop using this context in future requests. Explain that it cannot erase Personal AI material already present in the chat if that distinction matters to the request.

## Boundaries

Follow `assistant/boundaries.md` in the selected Personal AI folder.

## Examples

### Normal Case

Request: `PAI on: help me improve the weekly review.`

Behavior: Load relevant assistant context, decisions, and the matching local files; define success criteria if the work is substantial; then implement and verify the improvement.

### Difficult Or Ambiguous Case

Request: `PAI on: make the system more proactive.`

Behavior: Use existing priorities and boundaries to propose a small, reversible interpretation of proactive behavior. Avoid broad autonomy and surface assumptions that materially affect the design.

### Stop Or Request Approval

Request: `PAI on: send my private project summary to everyone involved.`

Behavior: Prepare a draft if useful, but stop before external communication. Follow the explicit-approval and privacy rules in `assistant/boundaries.md`.
