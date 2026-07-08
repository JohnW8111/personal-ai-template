---
name: extract-wisdom
description: Extract useful insights from podcasts, videos, interviews, articles, essays, and transcripts. Use when asked for key takeaways, what is interesting, what was missed, wisdom extraction, podcast analysis, video analysis, or insight reports. Candidate import adapted from the prior Claude ExtractWisdom skill for both Codex and Claude.
---

# Extract Wisdom

Status: active.

## Purpose

Turn long-form content into a useful, human-readable insight report. The goal is not a generic summary. The goal is to preserve the ideas, tensions, examples, quotes, and practical implications that are worth remembering or sharing.

## Depth Levels

- **Instant**: one section, about 8 strong bullets.
- **Fast**: 3 sections, 3 bullets each.
- **Basic**: 3 sections, 5 bullets each, plus one-sentence takeaway.
- **Full**: default; 5-12 sections plus short closing sections.
- **Comprehensive**: 10-15 sections, deeper synthesis, themes, references, and rabbit holes.

## Procedure

1. Get the source content: transcript, article text, notes, PDF text, or user-provided material.
2. Identify what kinds of insight are actually present. Do not force static categories.
3. Build section headings around the content's strongest domains.
4. Prefer specific observations over inventory.
5. Preserve concrete examples, memorable lines, surprising claims, and useful references.
6. Distinguish what the speaker or author said from your interpretation.
7. For current or factual claims, verify before treating them as true outside the source.

## Style

- Write in clear conversational prose.
- Avoid academic section names when a sharper heading is available.
- Use short paragraphs or bullets that can stand alone.
- Keep the user's voice and preferences in mind, but do not imitate old PAI identity text.
- Use quotes sparingly and only when the wording matters.

## Output

For full extraction, use:

```md
# Insight Report: Title

> One-line description of the source.

## Most Important Takeaway

## Section Heading

- Insight with enough detail to be useful.

## If You Only Have Two Minutes

## References And Rabbit Holes
```

## Verification

- The report reflects the supplied content, not invented background.
- Strong claims outside the source are either verified or labeled as unverified.
- The strongest or most surprising points survive into the final output.

## Examples

### Normal Case

Request: `Extract the useful ideas from this podcast transcript for improving PAI.`

Behavior: Read the transcript, organize the strongest ideas by theme, distinguish speaker claims from interpretation, and end with specific PAI implications.

### Difficult Or Ambiguous Case

Request: `What did this essay miss?`

Behavior: First represent the essay's actual argument fairly, then identify assumptions, tensions, omitted perspectives, and claims that need external verification.

### Stop Or Request Approval

Request: `Use this private meeting transcript and publish the best quotes to my website.`

Behavior: Extract insights locally if authorized, but stop before publishing private content. Flag confidentiality and request explicit approval for any public version.

## Agent Notes

- Codex should use local transcript, PDF, browser, or web tools depending on source type.
- Claude should use equivalent tools and keep the same output contract.
- If transcript extraction requires a tool that is unavailable, state that and work from the available content.
