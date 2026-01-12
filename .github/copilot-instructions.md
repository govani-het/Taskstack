# GitHub Copilot / AI Agent Instructions

Purpose: Give a short, actionable guide so an AI code assistant can be productive immediately in this training repository.

---

## Big picture
- This repository is a set of **independent learning modules** (folders like `01. foundations`, `03. frontend`, `11. react`, etc.). Each module is mostly self-contained and contains sample files, exercises and notes.
- Most content is **static** (HTML, images, text). There is no global build system, no package.json, and no test harness in the repository root.

## What to expect / How to work
- Open files in the relevant module you are changing. Example: `03. frontend/Task2.html` is a small static page that uses inline `<style>` and references assets from `03. frontend/images/` (e.g. `images/event.png`).
- Typical workflow: make small, focused edits inside a module folder, preview by opening the HTML in a browser (or use VS Code Live Server). There are no CI build steps to run locally for HTML-only modules.
- Many module folders include a `note.txt` intended for human/instructor guidance—check it first for module-specific instructions.

## Conventions observed
- Module folders are prefixed with a numeric order and a space (e.g. `03. frontend/`). Because folder names contain spaces, use quoting or escaped paths in shell commands.
- Asset folders live alongside tasks (e.g. `03. frontend/images/`). Use relative paths for assets (do not move assets without updating references in the same module).
- Styles are often implemented inline (a `<style>` block inside an HTML file). When introducing new shared styles across multiple tasks, prefer adding a module-level stylesheet (e.g. `03. frontend/styles.css`) rather than duplicating large style blocks.
- Repeated markup patterns are common—refactor cautiously to keep examples simple for learners (avoid over-abstracting instructors' examples unless asked).

## Concrete examples to reference
- `03. frontend/Task2.html`: uses a background image (`images/event.png`), multiple repeated `.rightside-inside-div` blocks, and inline CSS—good example of local asset referencing and small-page styling.
- Images: `03. frontend/images/` contains `.png`, `.webp`, `.avif`, `.jpg`, and `.mp4`—preserve formats and internal filenames when editing.

## When you add features or tooling
- If introducing JS tooling, tests, or a package manager, add clear documentation at the repository root (e.g., `README.md`) and include a `package.json` in the relevant module. Do not assume an existing workspace-level build environment.
- If adding a build step, keep it scoped to a specific module and document the specific commands to run (e.g., `cd "11. react" && pnpm install && pnpm dev`).

## PR & change guidance for an AI assistant
- Make small, reviewable changes per module (one learning task or small refactor per PR).
- Preserve the learning intent: avoid changing example structure unless fixing bugs, accessibility, or clarity, and add a short note in the PR describing why the change improves the lesson.

---

If you want, I can:
- Expand this file with per-module quick-start snippets (launch/preview commands), or
- Add a short checklist template for PRs that modifies learning materials.

Please tell me which you'd prefer or point me to a module to document next. ✅