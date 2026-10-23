# AGENTS.md

Rules every AI agent (and human contributor) must follow when working in this
repository. Sections `Technical Stack`, `Commands`, and `Architecture & Code
Style` are project-specific. `Guardrails & Boundaries` is generic — it must be
carried over unchanged when this file is reused in another project, and only
the first three sections are rewritten.

Standing approvals for autonomous work are recorded in
[`STANDING_APPROVALS.md`](STANDING_APPROVALS.md).

---

## Technical Stack

<!-- PROJECT SPECIFIC — regenerate when reusing this file in another project -->

- **Language/Runtime:** Python 3.12+ for template development (hooks, tests). Generated projects support 3.10–3.14.
- **Template engine:** cookiecutter ≥ 2.2 (CI verifies against 2.7.x), Jinja2 templating for all file/dir names and contents.
- **Generated-project toolchain:** uv (env + deps), hatchling build backend, PEP 621 `pyproject.toml`, src layout, ruff (lint + format), mypy, pytest + pytest-cov, pre-commit.
- **CI (this repo):** GitHub Actions — template render-matrix (default / docker=yes / license=Apache-2.0 permutations) on ubuntu-latest and windows-latest; generated output must pass ruff, mypy, pytest. Plus a repo lint job over `hooks/` and `tests/`.
- **Docs:** static Markdown in `docs/`, served by GitHub Pages from this repo (no custom domain in v1).
- **Testing:** pytest — hook unit tests plus render tests.
- **Quality gates:** ruff check, ruff format --check, mypy on `hooks/` and `tests/`.
- **License:** Apache 2.0 (template repo). Generated projects: MIT default, prompt-selectable (Apache-2.0, BSD-3-Clause, None/CC0).

**Legacy stack (old template, replaced by the 2026-10 rebuild):** venv + pip + `requirements/*.txt`, flake8/black/isort/autoflake, empty `src/main.py`, bash `setup.sh`, GPL-3.0, CC0 hardcoded for output. Do not build on it; the rebuild replaced it wholesale.

### Branch layout

- `main` — default/protected branch. Merges happen via PR only. (Legacy `prod`/`dev`/`stag` branches are archived history; nothing is deleted without explicit approval.)

---

## Commands

<!-- PROJECT SPECIFIC — regenerate when reusing this file in another project -->

Run all commands from the repository root unless stated otherwise.

```bash
# One-time repo dev setup
uv sync

# Render a project locally from this repo (no prompts, into a temp dir)
uvx cookiecutter . --no-input -o /tmp/render-test

# Interactive render (answers the 10 prompts)
uvx cookiecutter .

# Verify a generated project (run INSIDE the rendered output dir)
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
uv run pytest

# Quality gates for THIS repo (must be clean before every PR)
uv run ruff check hooks/ tests/
uv run ruff format --check hooks/ tests/
uv run mypy hooks/ tests/

# Tests for hooks
uv run pytest tests/
```

**Rule:** never invent commands. Use these verbatim. If a required command is
missing, check the CI workflow config first; if not defined anywhere, stop and
ask instead of guessing.

---

## Architecture & Code Style

<!-- PROJECT SPECIFIC — regenerate when reusing this file in another project -->

### Architecture

- `cookiecutter.json` — exactly 10 prompts: `project_name`, `package_name` (derived default, validated by the pre-gen hook to a valid identifier), `project_description`, `author`, `email`, `github_username`, `license` (MIT/Apache-2.0/BSD-3-Clause/None), `python_version` (3.10–3.14), `docker` (no/yes), `docs` (no/yes). No kitchen-sink prompt walls. `package_name` is also the generated directory name.
- `{{ cookiecutter.package_name }}/` — the rendered project: src-layout package with `__version__` + `add()` utility + matching test (pytest non-vacuous); `pyproject.toml` with ruff/mypy/pytest config inline; `.pre-commit-config.yaml`; templated README, LICENSE (per prompt, from `.license_templates/`), CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, `.gitignore`; `.github/workflows/ci.yml`; `Dockerfile` only when `docker=y`; mkdocs-material only when `docs=y`.
- `hooks/pre_gen_project.py` — validates the answered `package_name` (valid Python identifier, not a keyword); fails loudly with a clear ERROR line. (Note: `pre_prompt` runs *before* questions and cannot validate answers — do not use it for this.)
- `hooks/post_gen_project.py` — pure Python, Windows-safe: write LICENSE from `.license_templates/`; remove unselected docker/docs files; install deps via `uv sync`; `uv run pre-commit install`; `git init` + initial commit (uses `-c user.name/-c user.email` from prompts); run ruff/mypy/pytest; exit non-zero loudly on any failure; friendly error if `uv` or `git` is missing.
- `docs/` — GitHub Pages long-tail guides (4): "python cookiecutter template", "uv cookiecutter", "modern python project structure", "python boilerplate generator".
- `.github/workflows/` — `render-test.yml` matrix (permutations × OS) is the quality moat; `ci.yml` is the repo's own lint/type/test job. GitHub Actions `${{ }}` expressions inside generated workflow files must survive Jinja rendering (`{% raw %}`).
- Optionals (`docker`, `docs`) are rendered unconditionally and removed by the post-gen hook when not selected — one template, not forks.

### Code style

- Follow the existing pattern of the file/module you touch. Read neighboring code before writing anything new.
- Hooks formatted by ruff; type-hinted for mypy strictness over `hooks/` and `tests/`.
- Every behavior change (prompt, hook logic, generated file) ships with tests in the same PR; test names describe the behavior, not the implementation.
- Documentation (README, `docs/`) is updated in the same PR whenever prompts, generated layout, or setup behavior changes.
- No TODO markers, commented-out code, or dead files left behind.

---

## Guardrails & Boundaries

<!-- GENERIC — do not modify when reusing this file in another project -->

### 1. Anti-hallucination

- **Cite, never guess.** Every file, function, command, or config an agent
  references must exist in the repo right now — verify by reading before
  acting. No "it should probably be in…" reasoning.
- **No invented APIs.** Never use a library method from memory; read the
  installed package for the pinned version in use. Versions come from the
  manifests, not from recollection.
- **Read before edit.** A file must be fully read (not just grepped) before it
  is edited.
- **Verify before claiming.** Never say "done", "passing", or "fixed" without
  having run the actual command and seen real output.
- **Acknowledge unknowns.** Unsure about an env value, expected behavior, or
  secret? Stop and ask. Never invent credentials, URLs, or DB values.
- **No silent fallbacks.** If a step fails, report the real error verbatim.
  Do not work around it by editing unrelated files.
- **Diff-check after edits.** After every edit, review `git diff` to confirm
  only intended changes.

### 2. Scope discipline (no overreach)

- One issue = one PR = one logical change. Strictly implement only what the
  accepted issue defines (its AC).
- No drive-by refactors, renames, or formatting-only edits; no "while I'm in
  here" changes. Spotted problems → create a new issue, do not fix inline.
- No unrequested suggestions at the end of a task. Finish, report, stop.
  Ideas belong in GitHub issues.
- One-way decisions (schema changes, API contracts, migrations) are proposed
  in 1–3 lines and approved before applying.
- Never create `v2`, `copy`, `.new`, `backup`, or `-final` variants of files;
  edit in place.

### 3. Issue → branch → PR workflow

- Every task/feature starts as a GitHub issue before any code.
- Branch naming: `<type>/<issue#>-<slug>` (e.g. `feat/12-rate-limiting`).
- One task = one commit: conventional commits (`feat:`, `fix:`, `chore:`,
  `docs:`, `test:`), subject ≤ 50 chars, commit body ends with `refs #N`.
- Work happens on the issue branch; the PR targets the default branch.
- **PR checklist gates (all required before merge):**
  - tests pass (real command output),
  - ruff check / ruff format --check / mypy clean,
  - no secrets and no `.env` in the diff,
  - acceptance criteria demonstrably met,
  - docs updated if behavior/setup changed.
- Issue is closed **only** after its PR is merged. Never close otherwise.
- Never commit or PR directly to protected branches (`main`), even for docs.
  No skip-hooks (`--no-verify`), no force-pushing.

### 4. Task granularity & tracking

- One task = ≤ 30 minutes of work = one commit = one checkbox in its issue.
- A task exceeding 30 minutes is split into subtasks within the issue.
- Every task has executable acceptance criteria (a test, a command, or a
  demonstrable behavior). Done = AC passes — nothing more, nothing less.
- Feature issues are parents with a task checklist; each item is its own
  branch/PR and ≤ 30 minutes.
- Status is communicated through issue/PR comments, not memory or chat-only.

### 5. Security

- Never commit secrets, tokens, API keys, or `.env`; `.env` is git-ignored.
  Real secrets live only in the local `.env` / deployment secret store.
- Dependencies are added/changed only through the declared manifests
  (`pyproject.toml`); lockfile or pin updates are separate commits.
- Never disable lint, typecheck, or test gates to make something pass.

### 6. Destructive & irreversible operations

- The following require explicit, current-session user approval before
  running: `git push --force`, branch deletion, dropping/updating-down DB
  migrations, deleting files beyond the current task's scope, publishing or
  releasing, and anything modifying `main`/`prod` history.
- Never touch files outside the workspace directory.

### 7. On session start

- Read this file first.
- Check open issues and PRs to resume context; rely on issue/PR comments, not
  memory of a previous session.
- Confirm the target branch and issue number before the first action.
