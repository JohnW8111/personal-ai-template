# Claude / Cowork Capability Notes

Adapter-scoped notes for running this Personal AI system inside Claude (Claude
Code or the Cowork desktop app). These are execution details only. The canonical
workflows live in `skills/` and stay agent-neutral; nothing here changes a
skill's purpose, output contract, or verification requirements. Codex has its
own adapter under `adapters/codex/` and is unaffected by this file.

## Folder Access

- Claude only sees a folder after it is connected for the session. Access is per
  session and must be re-granted in each new Claude session.
- On a `PAI on` request without access, request this directory first, then
  proceed with the activation contract in `ON.md`.
- If your skills read archives outside this directory (briefings, transcripts,
  document collections), request those folders when a task needs them. The
  skill-specific source paths in each `SKILL.md` are authoritative; if a
  required archive is unavailable after a grant, ask where it moved rather than
  inventing content.

## Capability Map

How canonical skills can map to Claude/Cowork tools. Use these when available;
otherwise fall back to the neutral instructions in the skill.

- **Document and spreadsheet artifacts**: use the built-in `docx`, `xlsx`,
  `pptx`, and `pdf` skills to produce polished deliverables. Gather facts
  first, then read the relevant output-format skill before building the file.
- **Current facts and sources**: use the web search and fetch tools for recency
  and attribution. For JavaScript-rendered pages, use in-browser tools rather
  than a raw fetch.
- **Recurring runs** (`weekly-review`, briefings): offer to set these up as
  scheduled tasks. Scheduling is a convenience layer; the canonical workflow
  still produces the same output.
- **Deterministic helpers**: run the local tools directly, e.g.
  `python tools/weekly_review.py`. Prefer these over re-implementing a workflow
  by hand.

## Boundaries

- Follow `assistant/boundaries.md` exactly. Drafting is allowed; sending
  messages, spending money, executing trades, deleting important data, and
  publishing private context require explicit approval.
- Keep private context local. Do not move PAI material into external services
  without explicit approval.

## Parity Rule

Anything that materially changes a workflow belongs in the canonical skill (so
all assistants stay in sync), not in this file. Update the canonical skill
first, then adjust adapter execution details here only if needed.
