from __future__ import annotations

import hashlib
import fcntl
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import date, datetime
from html import escape
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


PERSONAL_AI_ROOT = Path(__file__).resolve().parents[1]
UI_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = UI_ROOT / "static"
BRIEFINGS_ROOT = Path.home() / "briefings"
PAI_REVIEWS_ROOT = PERSONAL_AI_ROOT / "reviews"
INBOX_PATH = PERSONAL_AI_ROOT / "inbox" / "README.md"

app = FastAPI(title="Personal AI")
app.mount("/static", StaticFiles(directory=STATIC_ROOT), name="static")


class FileUpdate(BaseModel):
    path: str
    content: str
    version: str


class FileCreate(BaseModel):
    path: str
    content: str = ""


class InboxCapture(BaseModel):
    thought: str


class PersonCreate(BaseModel):
    name: str


def resolve_markdown_path(relative_path: str) -> Path:
    if not relative_path or relative_path.startswith("/"):
        raise HTTPException(status_code=400, detail="Path must be relative.")

    path = (PERSONAL_AI_ROOT / relative_path).resolve()
    try:
        path.relative_to(PERSONAL_AI_ROOT)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Path escapes personal-ai.") from exc

    if "ui" in path.relative_to(PERSONAL_AI_ROOT).parts:
        raise HTTPException(status_code=400, detail="UI files are not editable here.")

    if path.suffix != ".md":
        raise HTTPException(status_code=400, detail="Only Markdown files are supported.")

    return path


def file_version(path: Path) -> str:
    if not path.exists():
        return "missing"
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    stat = path.stat()
    digest.update(str(stat.st_mtime_ns).encode("utf-8"))
    digest.update(str(stat.st_size).encode("utf-8"))
    return digest.hexdigest()


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


@contextmanager
def path_lock(path: Path):
    key = hashlib.sha256(str(path.resolve()).encode("utf-8")).hexdigest()
    lock_path = Path(tempfile.gettempdir()) / f"personal-ai-{key}.lock"
    with lock_path.open("a", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def local_today() -> str:
    return date.today().isoformat()


def read_title(path: Path, content: str | None = None) -> str:
    text = content if content is not None else path.read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def latest_morning_briefing() -> Path | None:
    if not BRIEFINGS_ROOT.exists():
        return None

    briefings = sorted(
        path
        for path in BRIEFINGS_ROOT.glob("*.md")
        if path.stem.count("-") == 2 and "weekly" not in path.stem.lower()
    )
    return briefings[-1] if briefings else None


def latest_pai_review() -> Path | None:
    if not PAI_REVIEWS_ROOT.exists():
        return None

    reviews = sorted(PAI_REVIEWS_ROOT.glob("*weekly-pai-review.md"))
    return reviews[-1] if reviews else None


def render_inline_markdown(text: str) -> str:
    links: list[str] = []

    def link_repl(match: re.Match[str]) -> str:
        label = escape(match.group(1))
        href = match.group(2).strip()
        if not href.startswith(("http://", "https://")):
            return label
        links.append(f'<a href="{escape(href, quote=True)}" target="_blank" rel="noreferrer">{label}</a>')
        return f"__LINK_{len(links) - 1}__"

    rendered = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    rendered = escape(rendered, quote=False)
    rendered = re.sub(r"`([^`]+)`", r"<code>\1</code>", rendered)
    rendered = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", rendered)
    for index, link in enumerate(links):
        rendered = rendered.replace(f"__LINK_{index}__", link)
    return rendered


def render_markdown(markdown: str) -> str:
    html: list[str] = []
    in_ul = False
    in_ol = False
    in_code = False
    code_lines: list[str] = []
    lines = markdown.splitlines()
    index = 0

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            html.append("</ul>")
            in_ul = False
        if in_ol:
            html.append("</ol>")
            in_ol = False

    def is_table_separator(line: str) -> bool:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)

    def table_cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            close_lists()
            if in_code:
                html.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            index += 1
            continue

        if in_code:
            code_lines.append(raw_line)
            index += 1
            continue

        if not stripped:
            close_lists()
            index += 1
            continue

        if "|" in stripped and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            close_lists()
            headers = table_cells(stripped)
            index += 2
            rows: list[list[str]] = []
            while index < len(lines):
                candidate = lines[index].strip()
                if not candidate or "|" not in candidate:
                    break
                rows.append(table_cells(candidate))
                index += 1
            html.append('<div class="table-wrap"><table><thead><tr>')
            html.extend(f"<th>{render_inline_markdown(cell)}</th>" for cell in headers)
            html.append("</tr></thead><tbody>")
            for row in rows:
                padded = row + [""] * max(0, len(headers) - len(row))
                html.append("<tr>")
                html.extend(f"<td>{render_inline_markdown(cell)}</td>" for cell in padded[: len(headers)])
                html.append("</tr>")
            html.append("</tbody></table></div>")
            continue

        if stripped == "---":
            close_lists()
            html.append("<hr />")
        elif stripped.startswith("### "):
            close_lists()
            html.append(f"<h3>{render_inline_markdown(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            close_lists()
            html.append(f"<h2>{render_inline_markdown(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            close_lists()
            html.append(f"<h1>{render_inline_markdown(stripped[2:])}</h1>")
        elif stripped.startswith("> "):
            close_lists()
            html.append(f"<blockquote>{render_inline_markdown(stripped[2:])}</blockquote>")
        elif stripped.startswith("- "):
            if in_ol:
                html.append("</ol>")
                in_ol = False
            if not in_ul:
                html.append("<ul>")
                in_ul = True
            html.append(f"<li>{render_inline_markdown(stripped[2:])}</li>")
        elif re.match(r"^\d+\.\s+", stripped):
            if in_ul:
                html.append("</ul>")
                in_ul = False
            if not in_ol:
                html.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\.\s+", "", stripped)
            html.append(f"<li>{render_inline_markdown(item)}</li>")
        else:
            close_lists()
            html.append(f"<p>{render_inline_markdown(stripped)}</p>")
        index += 1

    if in_code:
        html.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
    close_lists()
    return "\n".join(html)


def file_record(path: Path) -> dict[str, Any]:
    relative = path.relative_to(PERSONAL_AI_ROOT)
    stat = path.stat()
    parts = relative.parts
    section = parts[0] if len(parts) > 1 else "home"
    content = path.read_text(encoding="utf-8")
    summary = ""
    in_frontmatter = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or not stripped or stripped.startswith("#"):
            continue
        if ":" in stripped and len(stripped.split(":", 1)[0].split()) <= 2:
            continue
        summary = stripped
        break

    return {
        "path": relative.as_posix(),
        "title": read_title(path, content),
        "section": section,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
        "version": file_version(path),
        "summary": summary,
    }


def append_inbox_thought(thought: str) -> str:
    clean = " ".join(thought.split()).strip()
    if not clean:
        raise HTTPException(status_code=400, detail="Enter an idea before adding it.")
    if len(clean) > 1000:
        raise HTTPException(status_code=400, detail="Keep inbox ideas under 1,000 characters.")

    entry = f"- [ ] {local_today()} | {clean}"
    with path_lock(INBOX_PATH):
        content = INBOX_PATH.read_text(encoding="utf-8") if INBOX_PATH.exists() else "# PAI Inbox\n\n## Ideas\n"
        if "## Ideas" not in content:
            content = content.rstrip() + "\n\n## Ideas\n"
        ideas_heading = re.search(r"^## Ideas\s*$", content, flags=re.MULTILINE)
        if not ideas_heading:
            raise HTTPException(status_code=500, detail="Could not locate the Ideas section.")
        next_heading = re.search(r"^##\s+", content[ideas_heading.end():], flags=re.MULTILINE)
        insert_at = ideas_heading.end() + (next_heading.start() if next_heading else len(content[ideas_heading.end():]))
        before = content[:insert_at].rstrip()
        after = content[insert_at:].lstrip("\n")
        content = f"{before}\n\n{entry}\n"
        if after:
            content += f"\n{after}"
        atomic_write_text(INBOX_PATH, content)
    return entry


def slugify_person_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")


def person_template(name: str, today: str) -> str:
    return f"""# {name}

Status: active
Relationship:
Last updated: {today}

## Current Snapshot


## Last Call

Date:

Summary:

Follow-ups:

## Open Loops

-

## Next Call Prep

-

## Session Log

"""


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_ROOT / "index.html")


@app.get("/briefings/latest")
def latest_briefing() -> HTMLResponse:
    briefing = latest_morning_briefing()
    if not briefing:
        raise HTTPException(status_code=404, detail="No morning briefing found.")

    content = render_markdown(briefing.read_text(encoding="utf-8"))
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(briefing.name)}</title>
    <style>
      body {{
        margin: 0;
        background: #f7f9f8;
        color: #1c2421;
        font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      main {{
        max-width: 980px;
        margin: 0 auto;
        padding: 28px;
      }}
      .meta {{
        color: #62706b;
        font-size: 0.9rem;
        margin: 0 0 18px;
      }}
      a {{
        color: #0b5d4b;
      }}
      article {{
        border: 1px solid #d8e2de;
        border-radius: 8px;
        background: #ffffff;
        padding: 24px;
      }}
      h1, h2, h3 {{
        line-height: 1.25;
      }}
      h1 {{
        margin-top: 0;
      }}
      h2 {{
        border-top: 1px solid #d8e2de;
        margin-top: 28px;
        padding-top: 22px;
      }}
      li {{
        margin-bottom: 10px;
      }}
      blockquote {{
        border-left: 4px solid #127760;
        color: #33413d;
        margin: 16px 0;
        padding: 8px 0 8px 16px;
      }}
      code {{
        background: #eef6f3;
        border-radius: 4px;
        padding: 1px 4px;
      }}
      pre {{
        overflow-x: auto;
        background: #eef6f3;
        border-radius: 6px;
        padding: 14px;
      }}
      pre code {{
        padding: 0;
      }}
      .table-wrap {{
        overflow-x: auto;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
      }}
      th, td {{
        border: 1px solid #d8e2de;
        padding: 8px 10px;
        text-align: left;
        vertical-align: top;
      }}
      th {{
        background: #eef6f3;
      }}
    </style>
  </head>
  <body>
    <main>
      <p><a href="/">Back to Personal AI</a></p>
      <p class="meta">Latest briefing: {escape(briefing.name)}</p>
      <article>{content}</article>
    </main>
  </body>
</html>"""
    return HTMLResponse(html)


@app.get("/pai-review/latest")
def latest_weekly_pai_review() -> HTMLResponse:
    review = latest_pai_review()
    if not review:
        raise HTTPException(status_code=404, detail="No Weekly PAI Review found.")

    content = render_markdown(review.read_text(encoding="utf-8"))
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(review.name)}</title>
    <style>
      body {{
        margin: 0;
        background: #f7f9f8;
        color: #1c2421;
        font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      main {{
        max-width: 980px;
        margin: 0 auto;
        padding: 28px;
      }}
      .meta {{
        color: #62706b;
        font-size: 0.9rem;
        margin: 0 0 18px;
      }}
      a {{
        color: #0b5d4b;
      }}
      article {{
        border: 1px solid #d8e2de;
        border-radius: 8px;
        background: #ffffff;
        padding: 24px;
      }}
      h1, h2, h3 {{
        line-height: 1.25;
      }}
      h1 {{
        margin-top: 0;
      }}
      h2 {{
        border-top: 1px solid #d8e2de;
        margin-top: 28px;
        padding-top: 22px;
      }}
      li {{
        margin-bottom: 10px;
      }}
      blockquote {{
        border-left: 4px solid #127760;
        color: #33413d;
        margin: 16px 0;
        padding: 8px 0 8px 16px;
      }}
      code {{
        background: #eef6f3;
        border-radius: 4px;
        padding: 1px 4px;
      }}
      pre {{
        overflow-x: auto;
        background: #eef6f3;
        border-radius: 6px;
        padding: 14px;
      }}
      pre code {{
        padding: 0;
      }}
      .table-wrap {{
        overflow-x: auto;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
      }}
      th, td {{
        border: 1px solid #d8e2de;
        padding: 8px 10px;
        text-align: left;
        vertical-align: top;
      }}
      th {{
        background: #eef6f3;
      }}
    </style>
  </head>
  <body>
    <main>
      <p><a href="/">Back to Personal AI</a></p>
      <p class="meta">Latest Weekly PAI Review: {escape(review.name)}</p>
      <article>{content}</article>
    </main>
  </body>
</html>"""
    return HTMLResponse(html)


@app.get("/api/files")
def list_files() -> dict[str, Any]:
    files = [
        file_record(path)
        for path in PERSONAL_AI_ROOT.rglob("*.md")
        if "ui" not in path.relative_to(PERSONAL_AI_ROOT).parts
    ]
    files.sort(key=lambda item: (item["section"], item["path"]))
    return {"root": str(PERSONAL_AI_ROOT), "files": files}


@app.get("/api/file")
def read_file(path: str) -> dict[str, Any]:
    resolved = resolve_markdown_path(path)
    if not resolved.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    content = resolved.read_text(encoding="utf-8")
    return {
        "path": resolved.relative_to(PERSONAL_AI_ROOT).as_posix(),
        "title": read_title(resolved, content),
        "content": content,
        "modified": datetime.fromtimestamp(resolved.stat().st_mtime).isoformat(timespec="seconds"),
        "version": file_version(resolved),
    }


@app.post("/api/file")
def save_file(update: FileUpdate) -> dict[str, Any]:
    resolved = resolve_markdown_path(update.path)
    with path_lock(resolved):
        if not resolved.exists():
            raise HTTPException(status_code=404, detail="File not found.")
        if update.version != file_version(resolved):
            raise HTTPException(status_code=409, detail="File changed on disk. Reload before saving.")
        atomic_write_text(resolved, update.content)
    return file_record(resolved)


@app.post("/api/file/new")
def create_file(create: FileCreate) -> dict[str, Any]:
    resolved = resolve_markdown_path(create.path)
    with path_lock(resolved):
        if resolved.exists():
            raise HTTPException(status_code=409, detail="File already exists.")

        initial_content = create.content.strip()
        if not initial_content:
            title = resolved.stem.replace("-", " ").replace("_", " ").title()
            initial_content = f"# {title}\n\n"

        atomic_write_text(resolved, initial_content + ("\n" if not initial_content.endswith("\n") else ""))
    return file_record(resolved)


@app.post("/api/inbox")
def capture_inbox(capture: InboxCapture) -> dict[str, str]:
    return {"entry": append_inbox_thought(capture.thought)}


@app.post("/api/person")
def create_person(create: PersonCreate) -> dict[str, Any]:
    name = " ".join(create.name.split()).strip()
    if not name:
        raise HTTPException(status_code=400, detail="Person name needs at least one letter or number.")

    slug = slugify_person_name(name)
    if not slug:
        raise HTTPException(status_code=400, detail="Person name needs at least one letter or number.")

    path = resolve_markdown_path(f"people/active/{slug}.md")
    with path_lock(path):
        if path.exists():
            raise HTTPException(status_code=409, detail="Person file already exists.")
        atomic_write_text(path, person_template(name, local_today()))
    return file_record(path)


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8765, reload=False, app_dir=str(UI_ROOT))
