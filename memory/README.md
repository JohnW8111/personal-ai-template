# Memory

Use this directory for durable information that should change future assistant
behavior. Memory is selective, explicit, and reviewable; it is not a transcript.

## Explicit Capture

Use:

```text
PAI remember: concise fact, preference, decision, or lesson
```

The assistant should preserve the user's wording, add the date, and classify the
entry into the narrowest appropriate home:

- `decisions.md`: choices that should guide future work.
- `lessons.md`: reusable lessons learned from completed work.
- `feedback.md`: only explicit `PAI feedback` entries.
- `useful-context.md`: durable locations or context that does not fit elsewhere.
- `../background/preferences.md`: stable personal working preferences.
- `../background/`: durable domain, project, or recurring context.
- `../people/`: relationship-specific context.

If the destination or durability is unclear, place the statement in
`../inbox/README.md` for review instead of guessing.

## Capture Rules

- Record memory only after an explicit `PAI remember:` request.
- Do not infer memory from ordinary conversation, praise, frustration, or task history.
- Keep entries concise and factual.
- Do not duplicate information already stored in a more specific canonical file.
- Preserve private context locally.
- If new information conflicts with an active decision, preserve both records
  and mark the older decision `superseded`.

## Retrieval

For each PAI request, search memory using the request's:

- project or artifact name
- person or organization
- subject domain
- workflow or skill
- important action verbs and constraints

Load only relevant entries. Do not dump the entire memory directory into every
task when a focused search is sufficient.

## Review

During the Weekly PAI Review:

- flag missing absolute paths referenced by memory
- flag exact duplicate decision statements
- review recently completed work for durable lessons worth promoting
- identify context that is outdated, misplaced, or contradicted
- propose changes for review; do not rewrite durable memory automatically
