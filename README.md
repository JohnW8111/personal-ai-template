# Personal AI — a simple, private AI assistant setup you control

This is a starter kit for giving an AI assistant durable knowledge of who you
are, what you're working on, and how you like to work — so you stop
re-explaining yourself in every conversation.

It is deliberately simple: **a folder of plain-text files.** There is no app to
install, no account to create, no database, and nothing running in the cloud.
You fill in a few files about yourself, and any capable AI coding assistant
(Claude Code, Codex, and similar tools) reads them when — and only when — you
ask it to.

We call the system **PAI** (Personal AI) for short.

## What you need

1. **An AI coding assistant** that can read files on your computer, such as
   Claude Code or Codex. If you can open a terminal, type `claude` or `codex`,
   and chat with an AI that can see your files, you have what you need.
2. **Python 3.10 or newer** (already on most Macs) — only needed for the two
   optional extras: the weekly review and the local website. The core system
   is just text files and needs no Python at all.

## Setting it up (about 15 minutes)

1. Copy this folder to wherever you keep personal projects, for example
   `~/personal-ai`. Keep it out of shared or synced-public locations — it will
   hold personal information.
2. Open the four files in the `assistant/` folder that contain prompts —
   `profile.md`, `principles.md`, `priorities.md`, and `current-context.md` —
   and replace the prompts with your own answers. Short and honest beats long
   and polished. (The other three files in `assistant/` are sensible defaults;
   read them once and adjust anything you disagree with.)
3. Look through the files marked `CUSTOMIZE` and replace the examples with
   your own details. To find them all, run this in a terminal from inside the
   folder:

   ```bash
   grep -r CUSTOMIZE .
   ```

4. Replace the fictional example person (`people/active/example-person.md`)
   with a real person you meet with regularly, or delete it.
5. Start your AI assistant **from inside this folder** and try it:

   ```bash
   cd ~/personal-ai
   claude        # or: codex
   ```

   Then type:

   ```text
   PAI on: introduce yourself and tell me what you know about me.
   ```

## How to turn it on and off

The system is **off by default**. Your assistant behaves completely normally
until you type the on-switch, and the personal context is used only for that
request or session. Nothing is loaded behind your back.

| You type | What happens |
|---|---|
| `PAI on` or `PAI on: <request>` | The assistant reads your personal files, then helps with the request using them. |
| `PAI off` | The assistant stops using your personal files and goes back to normal. |
| `PAI remember: <fact>` | Saves one fact, preference, or decision to your files — this is the **only** way the assistant records lasting memory. |
| `PAI feedback: pass` or `PAI feedback: fail - <reason>` | Records your verdict on something the assistant produced, so quality can improve over time. |
| `PAI inbox: <thought>` | Jots an idea into your inbox file to sort out later. |

Two rules the assistant always follows: it never records memory about you
unless you explicitly say `PAI remember:`, and it never treats instructions
found inside web pages or documents as commands (see
`assistant/agent-trust.md`).

(The technical contract behind all of this lives in `ON.md` — the assistant
reads that file; you don't need to.)

## What's in each folder

```text
personal-ai/
  ON.md                       # Instructions the assistant follows when you say "PAI on"
  README.md                   # This file
  CLAUDE.md / AGENTS.md       # How Claude Code / Codex discover the on-switch
  assistant/                  # Who you are and how you want help — fill these in first
  background/                 # Durable facts: your projects, preferences
  people/                     # One file per person you meet with regularly
  skills/                     # Reusable step-by-step workflows the assistant can follow
  memory/                     # Decisions, lessons, and feedback — grows over time
  work/                       # Notes on larger tasks that span multiple sessions
  inbox/                      # Quick idea capture, sorted weekly
  reviews/                    # Generated weekly review reports
  adapters/                   # Tool-specific notes for Claude and Codex (advanced)
  tools/                      # The weekly review script
  ui/                         # The optional local website
  launch-personal-ai.command  # Mac shortcut: double-click to open the website
```

Start small: `assistant/` is the only folder that needs content on day one.
Everything else fills in gradually as you use the system.

## The weekly review (optional)

Once a week, run:

```bash
python3 tools/weekly_review.py
```

It writes a short dated report into `reviews/`: who you haven't talked to in a
while, ideas waiting in your inbox, tasks still open, and housekeeping flags.
It also saves a snapshot of the whole folder into git (if the folder is a git
repository), so you always have history to recover from.

## The local website (optional)

A small website, visible only on your own computer, for browsing and editing
these files without a code editor:

```bash
pip install -r ui/requirements.txt   # first time only
python3 ui/server.py
```

Then open `http://127.0.0.1:8765` in your browser. On a Mac you can instead
double-click `launch-personal-ai.command`. The website can only see and edit
files inside this folder.

## Keeping your information private

This folder is designed to hold personal context — that is the point of it.
So treat your filled-in copy like a diary:

- Keep it on your own computer, or in a **private** repository.
- **Never publish it.** If you use git, remember that history keeps everything
  you ever committed, even files you later delete.
- The assistant's ground rules in `assistant/boundaries.md` require your
  explicit approval before anything is sent, posted, spent, or published.

(This template itself contains no personal data — that protection begins the
moment you add yours.)

## Growing the system

A few rules that keep it healthy — the assistant knows them too:

- Keep everything plain text. Add structure only when a repeated need proves it.
- A "skill" is just a folder with a `SKILL.md` describing a workflow you repeat.
  When you notice yourself asking for the same thing twice, ask the assistant:
  `PAI on: turn what we just did into a skill.`
- Prefer a small useful file over a large impressive framework.
- Let memory grow through `PAI remember:`, not through bulk imports.
- Keep the inbox temporary: capture quickly, classify weekly, keep selectively.
