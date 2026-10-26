# AGENTS.md

Rules every AI agent (and human contributor) must follow when working in this
repository. Sections `Technical Stack`, `Commands`, and `Architecture & Code
Style` are project-specific. `Guardrails & Boundaries` is generic — it is
carried over unchanged when this file is reused in another project, and only
the first three sections are rewritten.

Standing approvals for autonomous work are recorded in
[`STANDING_APPROVALS.md`](STANDING_APPROVALS.md).

---

## Technical Stack

- **Language/Runtime:** Python {{ cookiecutter.python_version }}+.
- **Environment & dependencies:** uv (`.venv`, `uv.lock`, PEP 735 dependency
  groups); hatchling build backend; PEP 621 `pyproject.toml`; src layout.
- **Quality gates:** ruff (lint + format), mypy (strict), pytest with coverage,
  pre-commit.
- **CI:** GitHub Actions (`.github/workflows/ci.yml`) runs lint, format check,
  type check, and tests on every push and pull request.
- **License:** {{ cookiecutter.license }}.
- **Docs:** {% if cookiecutter.docs == "yes" %}mkdocs-material site in `docs/`{% else %}plain Markdown in `README.md`{% endif %}.

### Branch layout

- `main` — default/protected branch. Merges happen via PR only.

---

## Commands

Run all commands from the repository root.

```bash
# Environment + dependencies
uv sync

# Quality gates (must be clean before every PR)
uv run ruff check .
uv run ruff format --check .
uv run mypy src/
uv run pytest

# Pre-commit (same tools, one config)
uv run pre-commit run --all-files
{% if cookiecutter.docker == "yes" %}
# Container
docker build -t {{ cookiecutter.package_name }} .
{% endif %}
{% if cookiecutter.docs == "yes" %}
# Docs preview
uv sync --extra docs
uv run mkdocs serve
{% endif %}
```

**Rule:** never invent commands. Use these verbatim. If a required command is
missing, check the CI workflow config first; if not defined anywhere, stop and
ask instead of guessing.

---

## Architecture & Code Style

### Architecture

- `src/{{ cookiecutter.package_name }}/` — the package (src layout):
  `__init__.py` exposes `__version__` and the public API; `core.py` holds
  implementation.
- `tests/` — pytest suite; imports the installed package, never the repo root.
- `pyproject.toml` — PEP 621 metadata plus ruff/mypy/pytest configuration
  inline. No `requirements/*.txt`.
- `.pre-commit-config.yaml` — ruff, ruff-format, and mypy hooks.
- `.github/workflows/ci.yml` — CI gates.
{% if cookiecutter.docker == "yes" %}- `Dockerfile` + `.dockerignore` — multi-stage container build.
{% endif %}{% if cookiecutter.docs == "yes" %}- `docs/` + `mkdocs.yml` — mkdocs-material documentation site.
{% endif %}
### Code style

- Follow the existing pattern of the file/module you touch. Read neighboring
  code before writing anything new.
- Type hints required on public functions; mypy strict must stay clean.
- Every behavior change ships with tests in the same PR; test names describe
  the behavior, not the implementation.
- Documentation is updated in the same PR whenever behavior or setup changes.
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
  releasing, and anything modifying `main` history.
- Never touch files outside the workspace directory.

### 7. On session start

- Read this file first.
- Check open issues and PRs to resume context; rely on issue/PR comments, not
  memory of a previous session.
- Confirm the target branch and issue number before the first action.
