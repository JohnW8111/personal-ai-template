---
name: process-forge
description: Design or improve processes using DMADV, QFD, design thinking, human factors, process mapping, CTQ measures, stakeholder analysis, and FMEA. Use when asked to design a process, improve a workflow, map a process, build measures, identify failure modes, or coach through process redesign. Candidate import adapted from the prior Claude ProcessForge skill for both Codex and Claude.
---

# Process Forge

Status: active.

## Purpose

Guide process design and improvement work with practical structure. This skill is especially useful for healthcare, operations, consulting, and service workflows.

## Core Lenses

- **DMADV**: define, measure, analyze, design, verify.
- **QFD**: translate stakeholder needs into requirements.
- **Design thinking**: understand users, prototype, test.
- **Human factors**: design for real people under real constraints.
- **FMEA**: identify failure modes, effects, severity, occurrence, detection, and mitigations.

## Procedure

1. Clarify the process purpose, setting, users, constraints, and desired outcome.
2. Identify stakeholders and what each group needs from the process.
3. Map current state or draft future state.
4. Define critical-to-quality measures and success criteria.
5. Identify failure modes, risks, workarounds, handoffs, and human factors concerns.
6. Propose an improved process with roles, steps, decision points, measures, and verification plan.
7. Summarize open questions and next experiments.

## Output

Use the sections that fit the task:

```md
# Process Design: Name

## Aim

## Stakeholders And Needs

## Process Map

## Measures

## Failure Modes And Mitigations

## Proposed Design

## Verification Plan

## Next Actions
```

## Verification

- The proposed process maps back to the stated aim.
- Measures are observable, not vague.
- Failure modes include practical mitigation or detection.
- Human workload, handoffs, and edge cases are considered.

## Agent Notes

- Codex can create Markdown, diagrams, Mermaid maps, or structured JSON when useful.
- Claude should use the same framework and output contract.
- Keep the process lightweight unless the user asks for a full project artifact.
