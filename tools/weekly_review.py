from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from pathlib import Path


PERSONAL_AI_ROOT = Path(__file__).resolve().parents[1]
REVIEWS_ROOT = PERSONAL_AI_ROOT / "reviews"


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
            "- For a call, open the linked person file and use its open loops and next-call prep.",
            "- For cleanup, open the files listed above and update only what needs attention.",
            "- Keep this review as a prompt to act, not as another place to store durable notes.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    today = date.today()
    REVIEWS_ROOT.mkdir(parents=True, exist_ok=True)
    output = REVIEWS_ROOT / f"{today.isoformat()}-weekly-pai-review.md"
    output.write_text(build_review(today), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
