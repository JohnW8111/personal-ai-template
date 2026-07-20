# Personal AI — a private AI assistant that actually knows you

This is a starter kit for giving an AI assistant lasting knowledge of who you
are, what you care about, and what you're working on — so you stop
re-introducing yourself in every conversation.

It is deliberately simple: **a folder of ordinary files that lives on your own
computer.** There is no separate Personal AI account to create and nothing to
install beyond the AI app you already use. Your Personal AI files stay in this
folder on your computer; the AI app you choose may process conversations and
files you make available under its own privacy settings. Your AI assistant
uses the folder when — and only when — you ask it to.

We call the system **PAI** (Personal AI) for short.

## What you need

One of these AI desktop apps, already installed and working:

- **Claude** (the desktop app, using Cowork), or
- **ChatGPT** (the desktop app — you will use its **Codex** section)

If you can open one of those apps and have a conversation, you have everything
you need. No other software, and no technical skills.

## Setting it up (three steps, then a conversation)

**Step 1 — Get your copy of this folder.**
The easiest way: click this direct download link —
[**Download Personal AI**](https://github.com/JohnW8111/personal-ai-template/archive/refs/heads/main.zip).
(Or, on the GitHub page, click the green **Code** button and choose
**Download ZIP** — same thing. Do not use Fork, clone, or "Use this template"
unless you already understand GitHub and know how to keep your filled-in copy
private.)

Then look in your Downloads for a folder named `personal-ai-template-main`.
Some browsers deliver it as a ZIP file with that name instead — double-click
the ZIP and it becomes the folder. Move that whole folder somewhere easy to
find, like your **Documents** folder, and keep its name as-is. (You move the
whole folder — never just one file out of it.)

**Step 2 — Connect your AI app to the folder.**
- **Claude desktop app**: open Cowork and create a project using the existing
  folder you just moved. If Cowork asks which file to use as context, choose
  `START-HERE.md`. This is more reliable than attaching the folder to an
  ordinary conversation with the **+ Folder** button. If you already used
  **+ Folder**, you can still continue — use the Claude message in Step 3.
- **ChatGPT desktop app**: select **Codex** at the top of the app — not Chat.
  Codex is the part that can work inside your folder; regular Chat cannot see
  your files, so Personal AI will not work there. Then choose the folder you
  just moved as the place to work.

When you come back later, work in the same Cowork project or choose the same
folder in Codex, then type `PAI on` when you want to use it.

**Step 3 — Let the assistant interview you.**

In **Claude Cowork**, paste this first message:

```text
Use only the connected folder personal-ai-template-main. This is the Personal AI template in that folder, not Daniel Miessler's PAI or LifeOS. Do not search the web, download, or install anything for setup. Read START-HERE.md and follow it. Then begin the PAI setup interview one question at a time.
```

In **Codex**, type the same simple command as before:

```text
PAI setup
```

The assistant will ask you a few friendly questions — who you are, what you
care about, what you're working on, who you meet with regularly — and fill in
your files for you. It takes about 10–15 minutes, you can skip any question,
and you can stop and finish later. You never have to open or edit a file
yourself.

When the interview is done, try it out:

```text
PAI on: introduce yourself and tell me what you know about me.
```

## How to turn it on and off

The system is **off by default**. Your assistant behaves completely normally
until you type the on-switch. Once you turn it on, it stays on for that
workspace conversation until you type `PAI off`. A new conversation starts
off again. Nothing about you is loaded behind your back.

| You type | What happens |
|---|---|
| `PAI on` or `PAI on: <request>` | The assistant reads your personal files, then helps using what it knows about you. |
| `PAI off` | The assistant stops reading or using Personal AI files in future requests in this conversation. Start a new conversation for a clean separation from material already discussed. |
| `PAI remember: <something>` | Saves one durable fact, preference, decision, or lesson about you. |
| `PAI inbox: <a thought>` | Jots an idea down to sort out later. |
| `PAI feedback: pass` or `PAI feedback: fail - <why>` | Tells the system what worked and what didn't, so it improves. |

Two protections are built in: the assistant never turns ordinary conversation
into durable memory. `PAI setup`, `PAI remember:`, `PAI inbox:`, and `PAI
feedback:` each write only the specific information you explicitly ask them to
capture. It also never follows instructions it finds inside web pages or
documents — only yours.

## Everyday examples

```text
PAI on: help me get ready for my call with Maria tomorrow.
PAI on: what should I focus on this week?
PAI remember: my grandson's baseball games are Saturday mornings this fall.
PAI inbox: maybe a monthly letter to the family about what I'm learning.
PAI on: run my weekly review.
```

That last one produces a short weekly report — people you haven't talked to in
a while, ideas waiting in your inbox, tasks still open. Just ask for it; the
assistant handles the mechanics.

## What's in the folder (you don't need to memorize this)

- `assistant/` — who you are and how you want help (the interview fills this in)
- `people/` — one file per person or group you meet with regularly
- `background/` — lasting facts: your projects, interests, preferences
- `memory/` — decisions and lessons that accumulate over time
- `inbox/` — quick idea capture, sorted weekly
- `skills/` — step-by-step workflows the assistant can follow
- `work/`, `reviews/`, `tools/`, `adapters/` — supporting pieces the
  assistant uses; you can ignore them

The one file worth knowing about: `ON.md` is the instruction sheet the
assistant follows when you say `PAI on`. The assistant reads it; you don't
need to.

Nothing in this folder installs anything or runs on its own. Your AI app is
the only program involved — every file here is plain text you could open in
any editor.

## Keeping your information private

This folder will hold personal information — that is the point of it. Treat
your filled-in copy like a diary:

- Keep it on your own computer.
- Don't upload it, share it, or put it anywhere public.
- Don't put the filled-in folder in a shared cloud folder unless you are sure
  it is private.
- The assistant's ground rules (in `assistant/boundaries.md`) require your
  explicit approval before anything is ever sent, posted, spent, or published.

(This template contains no personal data — that protection matters from the
moment you add yours.)

## Growing it over time

Start small — the interview gives you everything you need for day one. As you
use it:

- When you catch yourself asking for the same kind of help twice, say:
  `PAI on: turn what we just did into a skill.` The assistant saves the
  workflow so next time is one sentence.
- When the assistant should know something for good, say `PAI remember:`.
- Once a week, say `PAI on: run my weekly review` and spend five minutes on
  what it surfaces.

The system grows by being used, not by being configured.
