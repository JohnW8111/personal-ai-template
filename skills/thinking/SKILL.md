---
name: thinking
description: Use structured thinking modes for first-principles analysis, root-cause work, creative ideation, red-team critique, council-style perspectives, hypothesis testing, and future/threat modeling. Use when asked to think deeply, decompose, challenge assumptions, brainstorm, critique, red team, weigh perspectives, or test an idea. Candidate import adapted from the prior Claude Thinking skill for both Codex and Claude.
---

# Thinking

Status: active.

## Purpose

Choose a thinking mode that matches the user's problem. This is a lightweight toolkit, not a mandate to overprocess simple requests.

## Modes

- **First principles**: decompose to fundamentals and rebuild from verified truths.
- **Root cause**: identify why a problem is happening before adding fixes.
- **Creative divergence**: generate varied options before converging.
- **Red team**: attack an idea, plan, argument, or investment thesis.
- **Council**: compare multiple perspectives without creating actual agents unless available and useful.
- **Hypothesis cycle**: goal, observe, hypothesize, test, measure, learn.
- **Future/threat model**: stress-test across time horizons and external changes.

## Procedure

1. Identify the question type and choose one or two modes.
2. State the frame briefly if it helps the user follow the analysis.
3. Generate the useful analysis, options, critique, or experiment plan.
4. Separate confident conclusions from assumptions.
5. End with a recommendation, decision criteria, or next experiment.

## Output Patterns

For first principles:

```md
## Problem
## Assumptions To Challenge
## Fundamentals
## Rebuilt Approach
## Recommendation
```

For red team:

```md
## Strongest Version Of The Idea
## Failure Modes
## Counterarguments
## What Would Change My Mind
## Better Version
```

For creative work:

```md
## Option Set
## Best Unusual Ideas
## Practical Shortlist
## Next Test
```

## Verification

- The mode chosen fits the actual request.
- The output does not pretend speculation is fact.
- Critique is useful and specific, not performative.
- Simple requests stay simple.

## Agent Notes

- Codex and Claude can both run this as pure reasoning.
- Do not require parallel agents. Simulate perspectives only when that is enough.
- If a decision involves current facts, pair this skill with `research`.
