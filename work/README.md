# Work Memory

Use this area for lightweight state on substantial tasks.

## When To Create A Work File

Create one when a task is multi-step, may span sessions, produces an important artifact, or contains decisions and unresolved questions worth preserving.

Do not create one for a simple answer, a small edit, or routine tool use that can be completed in one exchange.

## Locations

- `active/`: work that still has an unresolved next action.
- `completed/`: delivered and verified work retained for short-term reference.

Use filenames such as:

```text
active/2026-06-06-improve-pai-learning-loop.md
```

## Template

```md
# Work: Short Name

Status: active
Started: YYYY-MM-DD
Updated: YYYY-MM-DD

## Desired Outcome

## Success Criteria

- [ ] Observable result

## Current Status

## Decisions

- Decision and brief reason

## Open Questions

- Question or `None`

## Next Action

## Verification

- Evidence collected when a criterion is completed
```

## Rules

- Keep the file concise and current.
- Record conclusions and state, not chain-of-thought or a transcript.
- Link to canonical project files instead of duplicating them.
- Move the file to `completed/` after delivery and verification.
- Promote durable lessons or preferences to `memory/` only when they are likely to matter again.
