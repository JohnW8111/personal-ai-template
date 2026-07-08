# Personal AI — a small, file-based personal AI system

This is a template for a simple personal AI foundation that works with any
capable coding assistant (Codex, Claude Code, and similar tools). It is plain
Markdown and a couple of small Python helpers — no framework, no database, no
service to run.

The design goal is not a large "life operating system." It is a small set of
readable files that tell an assistant how to help you, where durable background
belongs, and which workflows should become reusable skills.

## Core ideas

- **Opt-in, never global.** The assistant uses this context only when you say
  `PAI on`. Otherwise it works normally.
- **One agent-neutral contract.** `ON.md` is the single source of truth for how
  the context loads. Codex and Claude read the same files.
- **Explicit memory only.** The assistant records durable memory only when you
  say `PAI remember:`, feedback only on `PAI feedback:`, ideas only on
  `PAI inbox:`. It never infers memory from ordinary conversation.
- **Skills are files.** A reusable workflow is a folder with a `SKILL.md` any
  assistant can read and follow.
- **Grow on proven need.** Start with the template, add structure only when a
  repeated need shows up.

## Structure

```text
personal-ai/
  ON.md                       # Opt-in switch and loading contract (single source of truth)
  README.md                   # This file
  CLAUDE.md                   # Claude Code discovery: what the switch means
  AGENTS.md                   # Codex discovery: what the switch means
  assistant/                  # How the assistant should work (fill these in first)
  background/                 # Durable facts and project context
  people/                     # Relationship and call-prep notes
  skills/                     # Agent-neutral reusable workflows
  memory/                     # Decisions, lessons, and useful context
  work/                       # Active and completed task state
  inbox/                      # Temporary capture awaiting triage
  reviews/                    # Generated Weekly PAI Reviews
  adapters/                   # Codex- and Claude-specific integration notes
  tools/                      # Deterministic local helpers (weekly review)
  ui/                         # Optional local editor and review website
  launch-personal-ai.command  # macOS launcher for the local UI
```

## Getting started

1. Clone or copy this directory to wherever you keep local projects.
2. Fill in the four personal files in `assistant/`: `profile.md`,
   `principles.md`, `priorities.md`, and `current-context.md`. Each contains
   prompts. (`boundaries.md`, `working-style.md`, and `agent-trust.md` ship
   with sensible defaults — adjust them to taste.)
3. Search the repository for `CUSTOMIZE` and replace the placeholders
   (external data paths, example entries).
4. Open the directory with your assistant and say:

   ```text
   PAI on: help me plan the first skill to add.
   ```

5. Add background, people, and skills gradually, as real use proves the need.

## The switch

- `PAI on` / `PAI on: <request>` — load this context for a request or session.
- `PAI off` — stop using it.
- `PAI remember: <fact>` — record explicit durable memory.
- `PAI feedback: pass|fail - <reason>` — record explicit feedback.
- `PAI inbox: <thought>` — capture an idea for later triage.

`ON.md` defines the full contract.

## Weekly review

```bash
python tools/weekly_review.py
```

Generates a dated review under `reviews/`: people needing follow-up, active
work, memory maintenance flags, inbox triage, and recent edits. It also prunes
old reviews (keeping the 2 newest) and auto-commits the directory to git so
your context always has local recovery history.

## Local UI (optional)

```bash
pip install -r ui/requirements.txt   # fastapi, uvicorn, pydantic (first time only)
python ui/server.py
```

Then open `http://127.0.0.1:8765` — a small local website for browsing and
editing these files, quick idea capture, and call preparation. It edits nothing
outside this folder.

## Privacy

This system is designed to hold personal context. Keep your filled-in copy
private: local disk, no remote, or a private repository. The template you are
reading contains no personal data; once you add yours, treat the directory as
confidential and never publish it (git history keeps everything you ever
committed).

## Design rules

- Keep the system plain text first.
- Do not add ceremony until a repeated need proves it.
- Keep skills agent-neutral and self-contained.
- Prefer a small useful file over a large abstract framework.
- Capture enough background to reduce repetition, not so much that maintenance
  becomes the work.
- Record durable memory and feedback only when explicitly asked.
- Keep the inbox temporary: capture quickly, classify later, retain selectively.
