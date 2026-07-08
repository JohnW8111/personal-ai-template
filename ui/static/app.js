const state = {
  files: [],
  currentPath: "",
  savedContent: "",
  version: "",
  dirty: false,
  editing: false,
  expandedSections: {},
};

const reviewCandidatesPath = "skills/README.md";
const sectionOrder = ["home", "assistant", "background", "memory", "inbox", "work", "people", "skills", "reviews", "adapters"];
const defaultSectionPaths = {
  home: ["README.md", "ON.md", "CLAUDE.md"],
  assistant: ["assistant/current-context.md", "assistant/working-style.md", "assistant/priorities.md"],
  background: ["background/projects.md", "background/preferences.md", "background/people.md"],
  inbox: ["inbox/README.md"],
  memory: ["memory/decisions.md", "memory/useful-context.md", "memory/lessons.md"],
  skills: ["skills/README.md", "skills/weekly-review/SKILL.md", "skills/research/SKILL.md"],
};

const rootPath = document.querySelector("#rootPath");
const fileList = document.querySelector("#fileList");
const searchInput = document.querySelector("#searchInput");
const newNoteButton = document.querySelector("#newNoteButton");
const newPersonButton = document.querySelector("#newPersonButton");
const reviewCandidatesButton = document.querySelector("#reviewCandidatesButton");
const inboxThought = document.querySelector("#inboxThought");
const addInboxButton = document.querySelector("#addInboxButton");
const personSelect = document.querySelector("#personSelect");
const openPersonButton = document.querySelector("#openPersonButton");
const prepCallButton = document.querySelector("#prepCallButton");
const updateCallButton = document.querySelector("#updateCallButton");
const promptOutput = document.querySelector("#promptOutput");
const copyPromptButton = document.querySelector("#copyPromptButton");
const sectionLabel = document.querySelector("#sectionLabel");
const fileTitle = document.querySelector("#fileTitle");
const filePath = document.querySelector("#filePath");
const editor = document.querySelector("#editor");
const editorGrid = document.querySelector("#editorGrid");
const preview = document.querySelector("#preview");
const saveButton = document.querySelector("#saveButton");
const reloadButton = document.querySelector("#reloadButton");
const toggleEditButton = document.querySelector("#toggleEditButton");
const dirtyBadge = document.querySelector("#dirtyBadge");
const statusLine = document.querySelector("#status");

function setStatus(message, kind = "") {
  statusLine.textContent = message;
  statusLine.className = `status ${kind}`.trim();
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function inlineMarkdown(value) {
  const links = [];
  const withPlaceholders = value.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, href) => {
    const trimmedHref = href.trim();
    if (!/^https?:\/\//i.test(trimmedHref)) return label;
    links.push(
      `<a href="${escapeHtml(trimmedHref)}" target="_blank" rel="noreferrer">${escapeHtml(label)}</a>`,
    );
    return `__LINK_${links.length - 1}__`;
  });
  let rendered = escapeHtml(withPlaceholders)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  links.forEach((link, index) => {
    rendered = rendered.replace(`__LINK_${index}__`, link);
  });
  return rendered;
}

function renderMarkdown(markdown) {
  const lines = markdown.split("\n");
  const html = [];
  let inList = false;
  let inOrderedList = false;
  let inCode = false;
  let codeLines = [];
  let index = 0;

  function closeList() {
    if (inList) {
      html.push("</ul>");
      inList = false;
    }
    if (inOrderedList) {
      html.push("</ol>");
      inOrderedList = false;
    }
  }

  function closeCode() {
    if (inCode) {
      html.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
      codeLines = [];
      inCode = false;
    }
  }

  function isTableSeparator(line) {
    const cells = line.trim().replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim());
    return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell));
  }

  function tableCells(line) {
    return line.trim().replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim());
  }

  while (index < lines.length) {
    const line = lines[index];
    if (line.trim().startsWith("```")) {
      if (inCode) {
        closeCode();
      } else {
        closeList();
        inCode = true;
      }
      index += 1;
      continue;
    }

    if (inCode) {
      codeLines.push(line);
      index += 1;
      continue;
    }

    if (!line.trim()) {
      closeList();
      index += 1;
      continue;
    }

    if (line.includes("|") && index + 1 < lines.length && isTableSeparator(lines[index + 1])) {
      closeList();
      const headers = tableCells(line);
      index += 2;
      const rows = [];
      while (index < lines.length && lines[index].trim() && lines[index].includes("|")) {
        rows.push(tableCells(lines[index]));
        index += 1;
      }
      html.push('<div class="table-wrap"><table><thead><tr>');
      html.push(...headers.map((cell) => `<th>${inlineMarkdown(cell)}</th>`));
      html.push("</tr></thead><tbody>");
      for (const row of rows) {
        const padded = [...row, ...Array(Math.max(0, headers.length - row.length)).fill("")];
        html.push("<tr>");
        html.push(...padded.slice(0, headers.length).map((cell) => `<td>${inlineMarkdown(cell)}</td>`));
        html.push("</tr>");
      }
      html.push("</tbody></table></div>");
      continue;
    }

    if (line.trim() === "---") {
      closeList();
      html.push("<hr />");
    } else if (line.startsWith("# ")) {
      closeList();
      html.push(`<h1>${inlineMarkdown(line.slice(2).trim())}</h1>`);
    } else if (line.startsWith("## ")) {
      closeList();
      html.push(`<h2>${inlineMarkdown(line.slice(3).trim())}</h2>`);
    } else if (line.startsWith("### ")) {
      closeList();
      html.push(`<h3>${inlineMarkdown(line.slice(4).trim())}</h3>`);
    } else if (line.startsWith("- ")) {
      if (inOrderedList) {
        html.push("</ol>");
        inOrderedList = false;
      }
      if (!inList) {
        html.push("<ul>");
        inList = true;
      }
      html.push(`<li>${inlineMarkdown(line.slice(2).trim())}</li>`);
    } else if (/^\d+\.\s+/.test(line)) {
      if (inList) {
        html.push("</ul>");
        inList = false;
      }
      if (!inOrderedList) {
        html.push("<ol>");
        inOrderedList = true;
      }
      html.push(`<li>${inlineMarkdown(line.replace(/^\d+\.\s+/, "").trim())}</li>`);
    } else if (line.startsWith("> ")) {
      closeList();
      html.push(`<blockquote>${inlineMarkdown(line.slice(2).trim())}</blockquote>`);
    } else {
      closeList();
      html.push(`<p>${inlineMarkdown(line.trim())}</p>`);
    }
    index += 1;
  }

  closeCode();
  closeList();
  preview.innerHTML = html.join("\n") || "<p>No content yet.</p>";
}

function setDirty(isDirty) {
  state.dirty = isDirty;
  saveButton.disabled = !state.currentPath || !isDirty || !state.editing;
  dirtyBadge.classList.toggle("hidden", !isDirty);
}

function setEditMode(isEditing) {
  state.editing = isEditing;
  editorGrid.classList.toggle("preview-only", !isEditing);
  toggleEditButton.textContent = isEditing ? "Preview" : "Edit";
  toggleEditButton.setAttribute("aria-pressed", String(isEditing));
  document.querySelectorAll(".edit-control").forEach((element) => {
    element.classList.toggle("hidden", !isEditing);
  });
  setDirty(state.dirty);
}

function toggleEditMode() {
  if (state.editing && state.dirty) {
    setStatus("Save or reload before hiding edit.", "error");
    return;
  }
  setEditMode(!state.editing);
}

function groupFiles(files) {
  return files.reduce((groups, file) => {
    const section = file.section || "home";
    groups[section] ||= [];
    groups[section].push(file);
    return groups;
  }, {});
}

function renderFileButton(file, parent) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `file-button ${file.path === state.currentPath ? "active" : ""}`;
  button.innerHTML = `<strong>${escapeHtml(file.title)}</strong><span>${escapeHtml(file.path)}</span>`;
  button.addEventListener("click", () => loadFile(file.path));
  parent.append(button);
}

function prioritizePaths(files, paths) {
  const priority = new Map(paths.map((path, index) => [path, index]));
  return [...files].sort((a, b) => {
    const aPriority = priority.has(a.path) ? priority.get(a.path) : Number.MAX_SAFE_INTEGER;
    const bPriority = priority.has(b.path) ? priority.get(b.path) : Number.MAX_SAFE_INTEGER;
    return aPriority - bPriority || a.path.localeCompare(b.path);
  });
}

function sortSectionFiles(section, files) {
  const sorted = [...files].sort((a, b) => a.path.localeCompare(b.path));
  if (section === "reviews") {
    return sorted.reverse();
  }
  if (section === "people") {
    return sorted.sort((a, b) => {
      const activeCompare = a.path.includes("/active/") === b.path.includes("/active/") ? 0 : a.path.includes("/active/") ? -1 : 1;
      return activeCompare || a.title.localeCompare(b.title);
    });
  }
  if (section === "work") {
    return sorted.sort((a, b) => {
      const rank = (file) => {
        if (file.path.startsWith("work/active/")) return 0;
        if (file.path === "work/README.md") return 1;
        if (file.path.startsWith("work/completed/")) return 3;
        return 2;
      };
      return rank(a) - rank(b) || a.path.localeCompare(b.path);
    });
  }
  if (defaultSectionPaths[section]) {
    return prioritizePaths(sorted, defaultSectionPaths[section]);
  }
  return sorted;
}

function defaultFilesForSection(section, files) {
  if (section === "reviews") {
    return files.slice(0, 1);
  }

  if (section === "work") {
    const activeWork = files.filter((file) => file.path.startsWith("work/active/"));
    if (activeWork.length) return activeWork.slice(0, 3);
  }

  if (section === "people") {
    const activePeople = files.filter((file) => file.path.includes("/active/"));
    if (activePeople.length) return activePeople.slice(0, 3);
  }

  const preferredPaths = defaultSectionPaths[section] || [];
  const preferred = preferredPaths
    .map((path) => files.find((file) => file.path === path))
    .filter(Boolean);
  if (preferred.length) return preferred.slice(0, 3);

  return files.slice(0, Math.min(3, files.length));
}

function visibleFilesForSection(section, files, query) {
  if (query || state.expandedSections[section]) return files;

  const visible = defaultFilesForSection(section, files);
  const currentFile = files.find((file) => file.path === state.currentPath);
  if (currentFile && !visible.some((file) => file.path === currentFile.path)) {
    return [...visible, currentFile];
  }
  return visible;
}

function sectionToggleText(section, isExpanded) {
  if (!isExpanded) return "Show all";
  return section === "reviews" ? "Show latest" : "Show less";
}

function renderFileSection(sectionElement, section, files, query) {
  const orderedFiles = sortSectionFiles(section, files);
  const defaultFiles = defaultFilesForSection(section, orderedFiles);
  const filesToShow = visibleFilesForSection(section, orderedFiles, query);
  const isExpanded = Boolean(state.expandedSections[section]);

  const heading = document.createElement("div");
  heading.className = "section-heading";

  const title = document.createElement("div");
  title.className = "section-title";
  title.textContent = `${section} (${orderedFiles.length})`;
  heading.append(title);

  if (orderedFiles.length > defaultFiles.length && !query) {
    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "section-toggle";
    toggle.textContent = sectionToggleText(section, isExpanded);
    toggle.setAttribute("aria-expanded", String(isExpanded));
    toggle.setAttribute("aria-label", `${isExpanded ? "Collapse" : "Expand"} ${section}`);
    toggle.addEventListener("click", () => {
      state.expandedSections[section] = !isExpanded;
      renderFileList();
    });
    heading.append(toggle);
  }

  sectionElement.append(heading);

  for (const file of filesToShow) {
    renderFileButton(file, sectionElement);
  }
}

function peopleFiles() {
  return state.files
    .filter((file) => /^people\/(active|inactive)\/[^/]+\.md$/.test(file.path))
    .sort((a, b) => {
      const statusCompare = a.path.includes("/active/") === b.path.includes("/active/") ? 0 : a.path.includes("/active/") ? -1 : 1;
      return statusCompare || a.title.localeCompare(b.title);
    });
}

function selectedPersonFile() {
  const path = personSelect.value;
  return peopleFiles().find((file) => file.path === path) || null;
}

function personName(file) {
  if (!file) return "";
  return file.title.replace(/\s+[—-]\s+Mentoring Notes$/i, "").trim();
}

function renderPersonPicker() {
  const people = peopleFiles();
  const previous = personSelect.value;
  personSelect.innerHTML = "";

  if (!people.length) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "No people yet";
    personSelect.append(option);
  } else {
    for (const file of people) {
      const option = document.createElement("option");
      const status = file.path.includes("/inactive/") ? "inactive" : "active";
      option.value = file.path;
      option.textContent = `${personName(file)} (${status})`;
      personSelect.append(option);
    }
    personSelect.value = people.some((file) => file.path === previous) ? previous : people[0].path;
  }

  const hasSelection = Boolean(personSelect.value);
  openPersonButton.disabled = !hasSelection;
  prepCallButton.disabled = !hasSelection;
  updateCallButton.disabled = !hasSelection;
}

function renderFileList() {
  const query = searchInput.value.trim().toLowerCase();
  const filtered = state.files.filter((file) => {
    const haystack = `${file.path} ${file.title} ${file.summary}`.toLowerCase();
    return !query || haystack.includes(query);
  });
  const groups = groupFiles(filtered);

  fileList.innerHTML = "";
  const sections = Object.keys(groups).sort((a, b) => {
    const aIndex = sectionOrder.indexOf(a);
    const bIndex = sectionOrder.indexOf(b);
    if (aIndex !== -1 || bIndex !== -1) {
      return (aIndex === -1 ? Number.MAX_SAFE_INTEGER : aIndex) - (bIndex === -1 ? Number.MAX_SAFE_INTEGER : bIndex);
    }
    return a.localeCompare(b);
  });

  for (const section of sections) {
    const sectionElement = document.createElement("section");
    sectionElement.className = "section";
    renderFileSection(sectionElement, section, groups[section], query);
    fileList.append(sectionElement);
  }

  if (!filtered.length) {
    fileList.innerHTML = '<p class="path">No matching files.</p>';
  }
}

async function loadFiles() {
  const response = await fetch("/api/files");
  if (!response.ok) throw new Error("Could not load file list.");
  const payload = await response.json();
  state.files = payload.files;
  rootPath.textContent = payload.root;
  renderFileList();
  renderPersonPicker();

  if (!state.currentPath && state.files.length) {
    const preferred = state.files.find((file) => file.path === "README.md") || state.files[0];
    await loadFile(preferred.path);
  }
}

async function loadFile(path) {
  if (state.dirty && !confirm("Discard unsaved changes?")) return;

  const response = await fetch(`/api/file?path=${encodeURIComponent(path)}`);
  if (!response.ok) {
    setStatus(`Could not load ${path}.`, "error");
    return;
  }

  const payload = await response.json();
  state.currentPath = payload.path;
  state.savedContent = payload.content;
  state.version = payload.version || "";

  sectionLabel.textContent = payload.path.includes("/") ? payload.path.split("/")[0] : "home";
  fileTitle.textContent = payload.title;
  filePath.textContent = payload.path;
  editor.value = payload.content;
  editor.disabled = false;
  toggleEditButton.disabled = false;
  reloadButton.disabled = false;
  setDirty(false);
  renderMarkdown(payload.content);
  renderFileList();
  setStatus(`Loaded ${payload.path}.`);
}

async function saveCurrentFile() {
  if (!state.currentPath) return;

  const response = await fetch("/api/file", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path: state.currentPath, content: editor.value, version: state.version }),
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    setStatus(detail.detail || "Save failed.", "error");
    return;
  }

  const saved = await response.json();
  state.savedContent = editor.value;
  state.version = saved.version || state.version;
  setDirty(false);
  setStatus(`Saved ${state.currentPath}.`, "success");
  await loadFiles();
}

async function createNewNote() {
  const rawPath = prompt("New Markdown path inside personal-ai/", "inbox/new-note.md");
  if (!rawPath) return;

  const path = rawPath.trim().replace(/^\/+/, "");
  if (!path.endsWith(".md")) {
    setStatus("New notes must end in .md.", "error");
    return;
  }

  const response = await fetch("/api/file/new", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ path }),
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    setStatus(detail.detail || "Could not create note.", "error");
    return;
  }

  await loadFiles();
  await loadFile(path);
  setStatus(`Created ${path}.`, "success");
}

async function captureInboxThought() {
  const thought = inboxThought.value.trim();
  if (!thought) {
    setStatus("Enter an idea before adding it.", "error");
    inboxThought.focus();
    return;
  }

  addInboxButton.disabled = true;
  const response = await fetch("/api/inbox", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ thought }),
  });
  addInboxButton.disabled = false;

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    setStatus(detail.detail || "Could not add the idea.", "error");
    return;
  }

  inboxThought.value = "";
  await loadFiles();
  if (state.currentPath === "inbox/README.md") {
    await loadFile(state.currentPath);
  }
  setStatus("Idea added to the PAI inbox.", "success");
  inboxThought.focus();
}

async function createNewPerson() {
  const rawName = prompt("Person name", "");
  if (!rawName) return;

  const name = rawName.trim();
  if (!name) {
    setStatus("Person name needs at least one letter or number.", "error");
    return;
  }

  const response = await fetch("/api/person", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    setStatus(detail.detail || "Could not create person.", "error");
    return;
  }

  const created = await response.json();
  await loadFiles();
  personSelect.value = created.path;
  renderPersonPicker();
  await loadFile(created.path);
  setStatus(`Created ${name}.`, "success");
}

async function openReviewCandidates() {
  await loadFile(reviewCandidatesPath);
}

async function copyText(value, successMessage) {
  promptOutput.value = value;
  copyPromptButton.disabled = false;

  try {
    await navigator.clipboard.writeText(value);
    setStatus(successMessage, "success");
  } catch {
    setStatus("Prompt is shown in the People / Calls box. Select and copy it manually.", "error");
  }
}

async function openSelectedPerson() {
  const file = selectedPersonFile();
  if (!file) return;
  await loadFile(file.path);
}

async function copyPrepPrompt() {
  const file = selectedPersonFile();
  if (!file) return;
  const name = personName(file);
  const prompt = `PAI on: prep me for my call with ${name}. Use ${file.path}. Focus on what we have been talking about, especially the last call, open loops, and the best questions for this call.`;
  await copyText(prompt, `Copied prep prompt for ${name}.`);
}

async function copyUpdatePrompt() {
  const file = selectedPersonFile();
  if (!file) return;
  const name = personName(file);
  const prompt = `PAI on: update ${name}'s notes from this call. Use ${file.path}. Preserve the existing history, update Last Call, Open Loops, Next Call Prep, and add a dated Session Log entry. Here are my rough notes:

`;
  await copyText(prompt, `Copied update prompt for ${name}.`);
}

async function copyVisiblePrompt() {
  if (!promptOutput.value) return;
  await copyText(promptOutput.value, "Copied prompt.");
}

editor.addEventListener("input", () => {
  renderMarkdown(editor.value);
  setDirty(editor.value !== state.savedContent);
});

searchInput.addEventListener("input", renderFileList);
saveButton.addEventListener("click", saveCurrentFile);
reloadButton.addEventListener("click", () => loadFile(state.currentPath));
toggleEditButton.addEventListener("click", toggleEditMode);
newNoteButton.addEventListener("click", createNewNote);
addInboxButton.addEventListener("click", captureInboxThought);
inboxThought.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
    event.preventDefault();
    captureInboxThought();
  }
});
newPersonButton.addEventListener("click", createNewPerson);
reviewCandidatesButton.addEventListener("click", openReviewCandidates);
personSelect.addEventListener("change", renderPersonPicker);
openPersonButton.addEventListener("click", openSelectedPerson);
prepCallButton.addEventListener("click", copyPrepPrompt);
updateCallButton.addEventListener("click", copyUpdatePrompt);
copyPromptButton.addEventListener("click", copyVisiblePrompt);

window.addEventListener("beforeunload", (event) => {
  if (!state.dirty) return;
  event.preventDefault();
  event.returnValue = "";
});

editor.disabled = true;
setEditMode(false);
loadFiles().catch((error) => {
  setStatus(error.message, "error");
});
