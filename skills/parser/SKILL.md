---
name: parser
description: Extract structured information from URLs, files, articles, newsletters, PDFs, transcripts, YouTube/video content, and pasted text. Use when asked to parse content, extract entities, produce JSON, detect content type, deduplicate entities, or convert unstructured material into a structured record. Candidate import adapted from the prior Claude Parser skill for both Codex and Claude.
---

# Parser

Status: active.

## Purpose

Convert messy source material into structured, auditable output. This skill is useful when the result needs to be reused in a database, spreadsheet, brief, or workflow.

## Content Types

- Pasted text.
- Article or web page.
- Newsletter.
- PDF or document text.
- YouTube/video transcript.
- Social post or thread.
- Batch list of sources.

## Procedure

1. Identify content type and source.
2. Extract raw text using the most reliable available tool.
3. Define the target schema before extraction when the user has not provided one.
4. Extract entities, dates, organizations, people, links, topics, claims, and source metadata as needed.
5. Preserve source references or offsets when auditability matters.
6. Validate JSON or structured output before returning it.
7. Flag duplicates, uncertain entities, missing fields, and extraction failures.

## Default JSON Shape

```json
{
  "source": {
    "type": "",
    "title": "",
    "url": "",
    "retrieved_at": ""
  },
  "summary": "",
  "entities": [],
  "claims": [],
  "links": [],
  "open_questions": []
}
```

## Verification

- JSON parses if JSON was requested.
- Required fields are present or explicitly null.
- Current URLs or documents are actually inspected.
- Uncertain extraction is marked rather than guessed.

## Agent Notes

- Codex should use structured parsers or libraries when available.
- Claude should use equivalent tools and preserve schema discipline.
- Do not invent transcript text, PDF text, URLs, or entity details.
