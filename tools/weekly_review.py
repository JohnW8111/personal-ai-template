from __future__ import annotations

import os
import re
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path


PERSONAL_AI_ROOT = Path(__file__).resolve().parents[1]
REVIEWS_ROOT = PERSONAL_AI_ROOT / "reviews"
# Customize this to your podcast transcript folder, or set PAI_TRANSCRIPTION_DATA_ROOT.
DEFAULT_TRANSCRIPTION_DATA_ROOT = Path("~/podcast-transcripts/data")
TRANSCRIPTION_DATA_ROOT = Path(
    os.environ.get("PAI_TRANSCRIPTION_DATA_ROOT", str(DEFAULT_TRANSCRIPTION_DATA_ROOT))
).expanduser()

PAI_PODCAST_KEYWORDS = {
    "personal ai": 9,
    "digital assistant": 9,
    "super assistant": 8,
    "personal agent": 9,
    "agent trust": 9,
    "zero trust": 9,
    "least agency": 9,
    "assistant": 5,
    "proactive": 8,
    "memory": 7,
    "memory poisoning": 9,
    "persistent context": 8,
    "context": 4,
    "context manipulation": 8,
    "workflow": 5,
    "workflows": 5,
    "agent": 4,
    "agents": 4,
    "coding agent": 6,
    "ai agent": 5,
    "automation": 5,
    "automate": 5,
    "autonomous": 4,
    "human-in-the-loop": 7,
    "governance": 6,
    "guardrails": 6,
    "prompt injection": 9,
    "red-team": 8,
    "red teaming": 8,
    "evaluation": 4,
    "evals": 5,
    "validation": 5,
    "verification": 6,
    "reliable": 3,
    "reliability": 3,
    "calibration": 6,
    "trust": 3,
    "policy": 3,
    "security": 4,
    "permissions": 5,
    "identity": 4,
    "file system": 5,
    "files": 2,
    "knowledge": 3,
    "world model": 7,
    "reasoning": 4,
    "certificate": 6,
    "second brain": 8,
    "agent os": 8,
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def title_from_markdown(path: Path) -> str:
    text = read_text(path)
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def field_value(text: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def section(text: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def bullets(text: str, limit: int = 5) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if item:
                items.append(item)
        if len(items) >= limit:
            break
    return items


def markdown_date(value: str) -> date | None:
    match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", value)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None


def latest_person_date(text: str) -> date | None:
    last_call = section(text, "Last Call")
    explicit = markdown_date(field_value(last_call, "Date"))
    if explicit:
        return explicit

    dates = [markdown_date(match.group(0)) for match in re.finditer(r"^###\s+20\d{2}-\d{2}-\d{2}", text, re.MULTILINE)]
    found = [item for item in dates if item]
    return max(found) if found else None


def bullet_field_value(text: str, field: str) -> str:
    match = re.search(rf"^-\s+{re.escape(field)}:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def person_reviews(today: date) -> list[dict[str, object]]:
    people: list[dict[str, object]] = []
    for path in sorted((PERSONAL_AI_ROOT / "people" / "active").glob("*.md")):
        text = read_text(path)
        last_date = latest_person_date(text)
        days = (today - last_date).days if last_date else None
        last_call = section(text, "Last Call")
        people.append(
            {
                "name": title_from_markdown(path),
                "path": path.relative_to(PERSONAL_AI_ROOT).as_posix(),
                "last_date": last_date,
                "days": days,
                "open_loops": bullets(section(text, "Open Loops"), limit=6),
            }
        )
    return people


def recent_files(today: date, limit: int = 8) -> list[Path]:
    files = [
        path
        for path in PERSONAL_AI_ROOT.rglob("*.md")
        if "ui" not in path.relative_to(PERSONAL_AI_ROOT).parts
        and "reviews" not in path.relative_to(PERSONAL_AI_ROOT).parts
    ]
    files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return files[:limit]


def memory_files() -> list[Path]:
    return sorted((PERSONAL_AI_ROOT / "memory").glob("*.md"))


def missing_memory_paths() -> list[dict[str, str]]:
    missing: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in memory_files():
        text = read_text(path)
        for match in re.finditer(r"`((?:/|~/)[^`]+)`", text):
            stored = match.group(1)
            resolved = Path(stored).expanduser()
            key = str(resolved)
            if key in seen or resolved.exists():
                continue
            seen.add(key)
            missing.append(
                {
                    "path": stored,
                    "source": path.relative_to(PERSONAL_AI_ROOT).as_posix(),
                }
            )
    return missing


def duplicate_decisions() -> list[str]:
    text = read_text(PERSONAL_AI_ROOT / "memory" / "decisions.md")
    decisions = [
        " ".join(match.group(1).split())
        for match in re.finditer(r"^- Decision:\s*(.+)$", text, flags=re.MULTILINE)
    ]
    counts: dict[str, int] = {}
    for decision in decisions:
        counts[decision] = counts.get(decision, 0) + 1
    return sorted(decision for decision, count in counts.items() if count > 1)


def recently_completed_work(today: date, days: int = 14) -> list[Path]:
    cutoff = today - timedelta(days=days)
    paths: list[tuple[date, Path]] = []
    for path in (PERSONAL_AI_ROOT / "work" / "completed").glob("*.md"):
        text = read_text(path)
        completed = (
            markdown_date(field_value(text, "Updated"))
            or markdown_date(path.name)
            or datetime.fromtimestamp(path.stat().st_mtime).date()
        )
        if cutoff <= completed <= today:
            paths.append((completed, path))
    paths.sort(key=lambda item: (item[0], item[1].name), reverse=True)
    return [path for _, path in paths]


def active_work_items() -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    work_root = PERSONAL_AI_ROOT / "work" / "active"
    for path in sorted(work_root.glob("*.md")):
        text = read_text(path)
        items.append(
            {
                "title": title_from_markdown(path).removeprefix("Work: ").strip(),
                "path": path.relative_to(PERSONAL_AI_ROOT).as_posix(),
                "status": field_value(text, "Status") or "active",
                "updated": field_value(text, "Updated") or "unknown",
                "outcome": " ".join(section(text, "Desired Outcome").splitlines()).strip(),
                "next_action": " ".join(section(text, "Next Action").splitlines()).strip(),
            }
        )
    return items


def explicit_feedback(limit: int = 10) -> list[dict[str, str]]:
    text = read_text(PERSONAL_AI_ROOT / "memory" / "feedback.md")
    pattern = re.compile(
        r"^##\s+(20\d{2}-\d{2}-\d{2})\s+-\s+(pass|fail)\s*$([\s\S]*?)(?=^##\s+|\Z)",
        flags=re.MULTILINE | re.IGNORECASE,
    )
    items: list[dict[str, str]] = []
    for match in pattern.finditer(text):
        body = match.group(3)
        items.append(
            {
                "date": match.group(1),
                "result": match.group(2).lower(),
                "context": bullet_field_value(body, "Context") or "Not specified",
                "feedback": bullet_field_value(body, "Feedback") or "No reason provided",
                "follow_up": bullet_field_value(body, "Follow-up") or "None",
            }
        )
    return items[-limit:][::-1]


def inbox_ideas(today: date) -> list[dict[str, object]]:
    text = read_text(PERSONAL_AI_ROOT / "inbox" / "README.md")
    pattern = re.compile(r"^-\s+\[\s\]\s+(20\d{2}-\d{2}-\d{2})\s+\|\s+(.+)$", flags=re.MULTILINE)
    items: list[dict[str, object]] = []
    for match in pattern.finditer(text):
        captured = markdown_date(match.group(1))
        if not captured:
            continue
        items.append(
            {
                "date": captured,
                "days": (today - captured).days,
                "thought": match.group(2).strip(),
            }
        )
    return items


def project_items() -> list[dict[str, str]]:
    text = read_text(PERSONAL_AI_ROOT / "background" / "projects.md")
    text = re.sub(r"```[\s\S]*?```", "", text)
    items: list[dict[str, str]] = []
    pattern = re.compile(r"^##\s+(.+?)\s*$([\s\S]*?)(?=^##\s+|\Z)", flags=re.MULTILINE)
    for match in pattern.finditer(text):
        title = match.group(1).strip()
        if title == "Project Template":
            continue
        body = match.group(2)
        items.append(
            {
                "title": title,
                "status": bullet_field_value(body, "Current status") or "Not specified",
                "next_action": bullet_field_value(body, "Next useful action") or "Not specified",
            }
        )
    return items


def summary_files() -> list[Path]:
    if not TRANSCRIPTION_DATA_ROOT.exists():
        return []
    return sorted(TRANSCRIPTION_DATA_ROOT.glob("*/summaries/*.md"))


def summary_date(path: Path, text: str) -> date | None:
    return (
        markdown_date(frontmatter_value(text, "date"))
        or markdown_date(path.name)
        or datetime.fromtimestamp(path.stat().st_mtime).date()
    )


def summaries_in_window(today: date, days: int = 7) -> list[tuple[Path, str, date]]:
    start = today - timedelta(days=max(days - 1, 0))
    in_window: list[tuple[Path, str, date]] = []
    for path in summary_files():
        text = read_text(path)
        dated = summary_date(path, text)
        if dated and start <= dated <= today:
            in_window.append((path, text, dated))
    return in_window


def line_score(line: str) -> int:
    lower = line.lower()
    return sum(weight for keyword, weight in PAI_PODCAST_KEYWORDS.items() if keyword in lower)


def podcast_summary_score(text: str, path: Path) -> int:
    score = line_score(text)
    name = path.name.lower().replace("-", " ")
    score += line_score(name) * 2
    if "key takeaways" in text.lower():
        score += 2
    return score


def relevant_podcast_lines(text: str, limit: int = 3) -> list[str]:
    candidates: list[tuple[int, str]] = []
    useful_sections = (
        "Key Takeaways",
        "Trend Signals",
        "Actionable Implications",
        "Open Questions / Uncertainty",
        "Open Questions",
    )
    current_section = ""
    for line in text.splitlines():
        stripped = line.strip()
        heading = re.match(r"^##\s+(.+?)\s*$", stripped)
        if heading:
            current_section = heading.group(1).strip()
            continue
        if not (stripped.startswith("- ") or stripped.startswith("> ")):
            continue
        item = stripped[2:].strip()
        score = line_score(item)
        if score:
            if current_section in useful_sections:
                score += 3
            candidates.append((score, item))
    candidates.sort(key=lambda item: item[0], reverse=True)
    selected: list[str] = []
    seen: set[str] = set()
    for _, line in candidates:
        normalized = " ".join(line.lower().split())
        if normalized in seen:
            continue
        seen.add(normalized)
        selected.append(line)
        if len(selected) >= limit:
            break
    return selected


def pai_implication(lines: list[str]) -> str:
    combined = " ".join(lines).lower()
    if "prompt injection" in combined or "poisoning" in combined or "least agency" in combined or "zero trust" in combined:
        return "Add an agent-trust check: limit tool/file access, treat untrusted inputs cautiously, and require approval before any external action."
    if "world model" in combined or "certificate" in combined or "reasoning" in combined or "verification" in combined:
        return "For substantial PAI outputs, include a compact evidence note with sources, assumptions, confidence, and needed approvals."
    if "governance" in combined or "guardrail" in combined or "policy" in combined:
        return "Make PAI boundaries explicit enough to enable useful work while preventing broad or silent autonomy."
    if "calibration" in combined or "reliab" in combined or "trust" in combined:
        return "Favor review surfaces and explicit user confirmation over autonomous action."
    if "memory" in combined or "context" in combined or "second brain" in combined:
        return "Keep improving durable local context, but make each context file directly useful for a recurring workflow."
    if "workflow" in combined or "automation" in combined or "automate" in combined:
        return "Turn repeated manual prompts into small scheduled reviews or website actions."
    if "agent" in combined or "assistant" in combined:
        return "Use narrow, named jobs with clear outputs instead of broad always-on agents."
    return "Consider whether this creates a small, local, low-noise improvement to PAI."


def podcast_signals(today: date, limit: int = 6) -> tuple[list[dict[str, object]], int, bool]:
    source_available = TRANSCRIPTION_DATA_ROOT.exists()
    summaries = summaries_in_window(today)
    ranked: list[tuple[int, Path, str, date]] = []
    for path, text, dated in summaries:
        score = podcast_summary_score(text, path)
        lines = relevant_podcast_lines(text)
        if lines:
            score += sum(line_score(line) for line in lines)
        if score >= 12:
            ranked.append((score, path, text, dated))

    ranked.sort(key=lambda item: (item[0], item[3], item[1].stat().st_mtime), reverse=True)
    signals: list[dict[str, object]] = []
    seen_titles: set[str] = set()
    for score, path, text, dated in ranked:
        title = frontmatter_value(text, "episode") or title_from_markdown(path)
        if title in seen_titles:
            continue
        lines = relevant_podcast_lines(text)
        if not lines:
            continue
        seen_titles.add(title)
        signals.append(
            {
                "score": score,
                "podcast": frontmatter_value(text, "podcast") or path.parents[1].name,
                "episode": title,
                "date": dated.isoformat(),
                "path": path.relative_to(TRANSCRIPTION_DATA_ROOT).as_posix(),
                "lines": lines,
                "implication": pai_implication(lines),
            }
        )
        if len(signals) >= limit:
            break
    return signals, len(summaries), source_available


def format_person(item: dict[str, object]) -> str:
    last_date = item["last_date"]
    days = item["days"]
    date_text = last_date.isoformat() if isinstance(last_date, date) else "unknown"
    stale = " - needs attention" if isinstance(days, int) and days >= 35 else ""
    lines = [
        f"- [{item['name']}](../{item['path']}): last call {date_text}"
        f"{f' ({days} days ago)' if isinstance(days, int) else ''}{stale}"
    ]
    open_loops = item["open_loops"]
    if open_loops:
        lines[0] += f"; {len(open_loops)} open loop(s)"

    return "\n".join(lines)


def build_review(today: date) -> str:
    people = person_reviews(today)
    stale_people = [item for item in people if isinstance(item["days"], int) and item["days"] >= 35]
    unknown_people = [item for item in people if item["days"] is None]
    work_items = active_work_items()
    feedback_items = explicit_feedback()
    failed_feedback = [item for item in feedback_items if item["result"] == "fail"]
    inbox_items = inbox_ideas(today)
    stale_inbox_items = [item for item in inbox_items if isinstance(item["days"], int) and item["days"] >= 14]
    current_context = read_text(PERSONAL_AI_ROOT / "assistant" / "current-context.md")
    projects = project_items()
    podcast_items, podcast_summary_count, transcription_source_available = podcast_signals(today)
    missing_paths = missing_memory_paths()
    repeated_decisions = duplicate_decisions()
    completed_work = recently_completed_work(today)

    lines = [
        f"# Weekly PAI Review - {today.isoformat()}",
        "",
        "## Quick Read",
        "",
        f"- Active people tracked: {len(people)}",
        f"- People needing attention: {len(stale_people) + len(unknown_people)}",
        f"- Active work items: {len(work_items)}",
        f"- Explicit feedback entries reviewed: {len(feedback_items)}",
        f"- Inbox ideas awaiting triage: {len(inbox_items)}",
        f"- Inbox ideas at least 14 days old: {len(stale_inbox_items)}",
        f"- Missing paths referenced by memory: {len(missing_paths)}",
        f"- Exact duplicate decision statements: {len(repeated_decisions)}",
        f"- Recently completed work files to check for lessons: {len(completed_work)}",
        f"- Podcast transcription source: {'available' if transcription_source_available else 'missing'}",
        "- Review scope: people, active work, memory, feedback, inbox, current context, projects, and recent Personal AI edits.",
        "",
        "## Suggested Attention This Week",
        "",
    ]

    if stale_people or unknown_people:
        for item in stale_people + unknown_people:
            name = item["name"]
            days = item["days"]
            if isinstance(days, int):
                lines.append(f"- Follow up on {name}: last call was {days} days ago.")
            else:
                lines.append(f"- Review {name}: no last-call date found.")
    else:
        lines.append("- No active people are past the 35-day follow-up threshold.")

    if stale_inbox_items:
        lines.append(
            f"- Decide whether to move, keep, merge, or discard {len(stale_inbox_items)} inbox idea(s) that are at least 14 days old."
        )
    elif inbox_items:
        lines.append(f"- Triage {len(inbox_items)} idea(s) in `inbox/README.md`.")

    if failed_feedback:
        lines.append(f"- Review {len(failed_feedback)} explicit feedback failure(s) for a possible skill, context, or workflow change.")

    if missing_paths:
        lines.append(f"- Repair or retire {len(missing_paths)} missing path reference(s) in memory.")

    if repeated_decisions:
        lines.append(f"- Merge or supersede {len(repeated_decisions)} exact duplicate decision statement(s).")

    if completed_work:
        lines.append(f"- Review {len(completed_work)} recently completed work file(s) for durable lessons.")

    lines.extend(["", "## People Follow-Up Radar", ""])
    if people:
        people.sort(key=lambda item: item["days"] if isinstance(item["days"], int) else 9999, reverse=True)
        lines.extend(format_person(item) for item in people)
        lines.extend(["", "Open the linked canonical person file for summaries, open loops, and call preparation."])
    else:
        lines.append("No active people files found.")

    lines.extend(["", "## Active Work", ""])
    if work_items:
        for item in work_items:
            lines.extend(
                [
                    f"### {item['title']}",
                    "",
                    f"- File: `{item['path']}`",
                    f"- Status: {item['status']}",
                    f"- Updated: {item['updated']}",
                ]
            )
            if item["outcome"]:
                lines.append(f"- Desired outcome: {item['outcome']}")
            if item["next_action"]:
                lines.append(f"- Next action: {item['next_action']}")
            lines.append("")
    else:
        lines.append("No active work files.")

    lines.extend(["", "## Memory Maintenance", ""])
    if missing_paths:
        lines.append("### Missing Paths")
        lines.append("")
        for item in missing_paths:
            lines.append(f"- `{item['path']}` referenced by `{item['source']}`")
        lines.append("")
    else:
        lines.append("- No missing absolute paths found in memory.")

    if repeated_decisions:
        lines.extend(["", "### Duplicate Decisions", ""])
        lines.extend(f"- {decision}" for decision in repeated_decisions)
    else:
        lines.append("- No exact duplicate decision statements found.")

    if completed_work:
        lines.extend(["", "### Completed Work To Review For Lessons", ""])
        for path in completed_work:
            rel = path.relative_to(PERSONAL_AI_ROOT).as_posix()
            lines.append(f"- [{title_from_markdown(path)}](../{rel})")
        lines.append("")
        lines.append(
            "Promote only lessons that would change future behavior; do not copy task summaries into memory."
        )
    else:
        lines.append("- No recently completed work files need a lesson review.")

    lines.extend(
        [
            "",
            "Review outdated, misplaced, or contradicted context manually. Do not rewrite durable memory automatically.",
        ]
    )

    lines.extend(["", "## Recent Explicit Feedback", ""])
    if feedback_items:
        for item in feedback_items:
            lines.extend(
                [
                    f"### {item['date']} - {item['result']}",
                    "",
                    f"- Context: {item['context']}",
                    f"- Feedback: {item['feedback']}",
                    f"- Follow-up: {item['follow_up']}",
                    "",
                ]
            )
    else:
        lines.append("No explicit PAI feedback recorded.")

    lines.extend(["", "## Inbox", ""])
    if inbox_items:
        lines.append("> Capture quickly, classify later, retain selectively.")
        lines.append("")
        for item in sorted(inbox_items, key=lambda entry: entry["date"]):
            stale = " - decision needed" if item["days"] >= 14 else ""
            lines.append(f"- {item['date'].isoformat()} ({item['days']} days old){stale}: {item['thought']}")
        lines.extend(
            [
                "",
                "For each idea: move it to its proper home, keep it temporarily, merge it, or discard it.",
            ]
        )
    else:
        lines.append("No ideas awaiting triage.")

    lines.extend(["", "## Current Context", ""])
    focus = section(current_context, "Current Focus")
    questions = section(current_context, "Open Questions")
    if focus:
        lines.append("### Current Focus")
        lines.append(focus)
        lines.append("")
    if questions:
        lines.append("### Open Questions")
        lines.append(questions)
    if not focus and not questions:
        lines.append("No current context focus or questions found.")

    lines.extend(["", "## Projects", ""])
    if projects:
        lines.append("- [Canonical project context](../background/projects.md)")
        for item in projects:
            line = f"- **{item['title']}**: status {item['status']}"
            if item["next_action"] != "Not specified":
                line += f"; next action {item['next_action']}"
            lines.append(line)
    else:
        lines.append("No project background found.")

    lines.extend(["", "## Podcast Signals For PAI Improvement", ""])
    if not transcription_source_available:
        lines.append(
            f"Podcast signals were not checked because the configured transcription source does not exist: `{TRANSCRIPTION_DATA_ROOT}`."
        )
        lines.append(
            "Restore that location or set `PAI_TRANSCRIPTION_DATA_ROOT` before running the review."
        )
    elif podcast_items:
        lines.append(
            f"These are not general podcast summaries. They are signals from the last 7 days of saved podcast summaries ({podcast_summary_count} summary files in scope) that look relevant to making PAI more useful, bounded, and proactive."
        )
        lines.append("")
        for item in podcast_items:
            lines.extend(
                [
                    f"### {item['episode']}",
                    "",
                    f"- Podcast: {item['podcast']}",
                    f"- Episode date: {item['date']}",
                    f"- Source: `transcription/data/{item['path']}`",
                    f"- PAI implication: {item['implication']}",
                    "- Relevant signals:",
                ]
            )
            lines.extend(f"  - {line}" for line in item["lines"])
            lines.append("")
    else:
        lines.append(
            f"No podcast summary signals found for PAI improvement in `{TRANSCRIPTION_DATA_ROOT}`."
        )

    lines.extend(["", "## Recent Personal AI Edits", ""])
    for path in recent_files(today):
        modified = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        rel = path.relative_to(PERSONAL_AI_ROOT).as_posix()
        lines.append(f"- `{rel}` - {modified}")

    lines.extend(
        [
            "",
            "## How To Use This",
            "",
            "- For a call, use the People / Calls panel in the Personal AI website.",
            "- For cleanup, open the files listed above and use `Edit` only when needed.",
            "- Keep this review as a prompt to act, not as another place to store durable notes.",
            "",
        ]
    )
    return "\n".join(lines)


def prune_reviews(keep: int = 2) -> None:
    """Keep only the newest reviews; older ones stay retrievable via git history."""
    reviews = sorted(REVIEWS_ROOT.glob("*-weekly-pai-review.md"))
    for path in reviews[:-keep] if keep else reviews:
        path.unlink()
        print(f"Pruned old review: {path.name}")


def commit_personal_ai(today: date) -> None:
    """Optional git checkpoint for advanced users who explicitly enable it."""

    if os.environ.get("PAI_WEEKLY_REVIEW_AUTO_COMMIT") != "1":
        print("Auto-commit skipped: set PAI_WEEKLY_REVIEW_AUTO_COMMIT=1 to enable.")
        return

    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(PERSONAL_AI_ROOT), *args],
            capture_output=True,
            text=True,
        )

    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        print("Auto-commit skipped: the Personal AI folder is not inside a git repository.")
        return
    if not git("status", "--porcelain", "--", ".").stdout.strip():
        print("Auto-commit: no Personal AI changes to commit.")
        return
    git("add", "-A", "--", ".")
    # The trailing pathspec limits the commit to this folder, leaving anything
    # staged elsewhere in the repository untouched.
    result = git(
        "commit",
        "-m",
        f"Weekly PAI review auto-commit {today.isoformat()}",
        "--",
        ".",
    )
    if result.returncode == 0:
        print(f"Auto-commit: committed personal-ai changes ({today.isoformat()}).")
    else:
        detail = result.stderr.strip() or result.stdout.strip()
        print(f"Auto-commit failed: {detail}")


def main() -> None:
    today = date.today()
    REVIEWS_ROOT.mkdir(parents=True, exist_ok=True)
    output = REVIEWS_ROOT / f"{today.isoformat()}-weekly-pai-review.md"
    output.write_text(build_review(today), encoding="utf-8")
    print(output)
    prune_reviews()
    commit_personal_ai(today)


if __name__ == "__main__":
    main()
