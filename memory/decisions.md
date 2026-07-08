# Decisions

Record decisions that should guide future work.

## Entry Format

New decisions should use:

```md
### Short decision title

- Status: active
- Decision: What should guide future work.
- Reason: Why this choice was made.
```

Use `Status: active` or `Status: superseded`. When a decision changes, keep the
old entry, mark it superseded, and add:

```md
- Superseded by: YYYY-MM-DD - Short decision title
```

## Example (replace with your own)

### Keep the personal AI system plain text first

- Status: active
- Decision: Prefer Markdown files and small scripts over databases and services.
- Reason: Readability and low maintenance matter more than features at this stage.
