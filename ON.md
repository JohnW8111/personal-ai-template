# PAI On

Use this file as the opt-in switch for the personal AI context.

## Canonical System

`PAI on` always means the folder containing this `ON.md` file. The first
context layer is `assistant/`, and all Markdown files in that directory must be
read before the request is interpreted.

If this folder cannot be found, ask where it moved instead of silently
substituting another directory.

## Switch Phrase

```text
PAI on
```

Use it at the start of a request:

```text
PAI on: help me plan the next skill to add.
```

The explicit capture commands `PAI remember:`, `PAI feedback:`, and
`PAI inbox:` also activate this system for that capture. `PAI setup` activates
it and starts the first-run interview in `skills/setup/SKILL.md`.

## What The Assistant Should Do

When the user invokes `PAI on`, the assistant should:

1. Resolve `PAI on` to the folder containing this `ON.md` file.
2. Read every Markdown file in `assistant/` before interpreting the request.
3. Read `skills/README.md` and decide whether a shared skill matches the request.
4. If a skill matches, read that skill's `SKILL.md` and use it as the canonical workflow.
5. Search `background/` only for relevant durable context.
6. Search `memory/` using the request's project, person, domain, workflow, and constraint terms.
7. Search `people/` for relationship or call context when relevant.
8. Use tool-specific adapters only when the canonical skill needs Codex- or Claude-specific execution details.
9. For a substantial task, state a small set of testable success criteria and create or update a work file only when durable task state will help.
10. If the user says `PAI remember: <memory>`, classify and record it using `memory/README.md`.
11. If the user gives explicit `PAI feedback`, append it to `memory/feedback.md`.
12. If the user says `PAI inbox: <thought>`, append a dated unchecked entry under `## Ideas` in `inbox/README.md`.
13. Briefly say that PAI context is loaded, name any skill being used, then proceed with the task.

## Substantial Tasks

A task is substantial when it is multi-step, spans sessions, produces an important artifact, or contains decisions and unresolved questions worth preserving.

For these tasks:

- Identify 2-5 observable completion criteria.
- Keep the criteria proportional to the task; do not turn a simple request into a planning exercise.
- Create `work/active/YYYY-MM-DD-short-name.md` only when the state may be useful after the current exchange.
- Move the file to `work/completed/` when the outcome is delivered and verified.

## Explicit Feedback

The supported forms are:

```text
PAI feedback: pass
PAI feedback: pass - concise reason
PAI feedback: fail - what was missed
```

Record only explicit feedback. Do not infer sentiment or silently convert ordinary comments into durable memory.

## Explicit Memory

The supported form is:

```text
PAI remember: concise fact, preference, decision, or lesson
```

Classify the entry using `memory/README.md`. Record it directly when
the destination is clear. If it conflicts with an active decision, mark the old
decision superseded and link the two entries. If durability or destination is
unclear, place it in the inbox for review. Do not infer memory from ordinary
conversation.

## Quick Inbox Capture

The supported form is:

```text
PAI inbox: idea or thought
```

Append it as:

```md
- [ ] YYYY-MM-DD | idea or thought
```

Keep the wording close to the user's original thought. Do not classify, expand, or promote it during capture unless the user asks.

## Skill Selection

The assistant should consider shared skills before improvising a workflow. A skill is relevant when its `description` or entry in `skills/README.md` matches the user's intent.

Examples:

- `PAI setup` -> use `skills/setup/SKILL.md` (first-run interview; also offer it when `assistant/` still contains template prompts).
- `PAI on: run my weekly review` -> use `skills/weekly-review/SKILL.md`.
- `PAI on: extract wisdom from this podcast` -> use `skills/extract-wisdom/SKILL.md`.
- `PAI on: research this decision` -> use `skills/research/SKILL.md`.
- `PAI on: design a better intake process` -> use `skills/process-forge/SKILL.md`.

If no skill fits, the assistant should handle the request normally while still using relevant assistant, background, and memory context.

## Scope

This is opt-in. Once the user says `PAI on`, keep the Personal AI context active
for the rest of that workspace conversation, until they say `PAI off`.

Every new conversation starts off. If the user does not invoke the switch, the
assistant should work normally.

## Turn It Off

Use:

```text
PAI off
```

This stops future reading or use of Personal AI files in the current
conversation. It cannot erase Personal AI material already present in the chat;
start a new conversation for a clean separation.

## Legacy Alias

`Personal AI on` and `Personal AI off` still mean the same thing, but `PAI on` and `PAI off` are the preferred forms.
