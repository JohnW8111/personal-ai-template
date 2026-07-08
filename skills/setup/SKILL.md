---
name: setup
description: First-run guided setup. Interview the user in plain language and fill in their personal files for them. Use when the user says "PAI setup", "set up my personal AI", "get started", "interview me", "help me set this up", or when the assistant notices the assistant/ files still contain template prompts and the user seems new.
---

# Setup Interview

## Purpose

Turn the blank template into the user's own Personal AI by interviewing them —
so they never have to open or edit a file themselves. The user may have no
technical background at all. Assume they have never heard of Markdown, git, or
a terminal, and never mention those things unless they ask.

## Ground Rules

- Ask **one question at a time**. Wait for the answer before asking the next.
- Use warm, plain language. No jargon.
- Short answers are fine. Never pressure the user to write more.
- If the user skips a question, leave that part of the template as-is and move on.
- Read back a short summary before writing anything, and confirm it sounds right.
- Never invent answers the user did not give.
- The whole interview should take 10–15 minutes. Offer to pause anytime and
  resume later with `PAI setup` — on resume, skip questions already answered
  (check whether the files still contain template prompts).

## Interview Flow

Open with one or two sentences: you are going to ask a few questions so this
folder can become their personal AI, and they can say "skip" to any question.

**1. About them** (writes to `assistant/profile.md`)
- What should I call you?
- In a sentence or two, who are you? (Work, retired, volunteering, family — whatever matters to you.)
- What made you want a personal AI? What do you hope it helps with?

**2. What they care about** (writes to `assistant/principles.md`)
- Are there values or principles you'd want guiding any advice I give you?
  (Faith, family, honesty, generosity — whatever is true for you.)

**3. What they're working on** (writes to `assistant/priorities.md` and `assistant/current-context.md`)
- What are the two or three things you most want to make progress on right now?
- Anything coming up soon that's on your mind?

**4. How they like to be helped** (writes to `assistant/working-style.md` — append, don't replace the defaults)
- Do you prefer short answers or detailed explanations?
- Anything that annoys you about how AI assistants usually respond?

**5. People** (writes to `people/active/`)
- Is there someone you meet or talk with regularly — a friend, mentee, group —
  you'd like help preparing for and remembering details about? (If yes, create
  a person file using the pattern in `people/active/example-person.md`, then
  ask whether to delete the example file. If no, just offer to delete the
  example file.)

**6. Interests for the future** (writes to `background/preferences.md`)
- Any topics you'd want me to keep an eye on or know you care about?

## After Writing

1. Update each file, replacing the template prompts and any `CUSTOMIZE` notes
   that the interview answered. Leave unanswered sections for a future session.
2. Read back a one-paragraph summary: "Here's what your Personal AI now knows
   about you..." and invite corrections.
3. Teach the five commands in one short list, with a one-line plain
   explanation each: `PAI on`, `PAI off`, `PAI remember:`, `PAI inbox:`,
   `PAI feedback:`.
4. End by inviting them to try it immediately:

   ```text
   PAI on: introduce yourself and tell me what you know about me.
   ```

## Verification

- Every file the interview touched contains the user's actual words or a
  faithful summary of them — no template prompts remain in answered sections.
- Nothing was written that the user did not say or confirm.
- The user was shown the summary and the five commands.
