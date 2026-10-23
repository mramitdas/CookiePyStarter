# Agent Permissions — Standing Approvals

This file records approval the repository owner granted in-session
(2026-10-23) so agents do not need to wait for per-action confirmation.
It is referenced by `AGENTS.md` (Guardrails & Boundaries).

## Standing approvals (pre-authorized)

- Creating/deleting agent-created branches (`<type>/<issue#>-<slug>`).
- Commits, pushes to agent-created branches, and `origin` remote operations.
- Creating/updating/closing GitHub issues and comments.
- Creating PRs targeting the default branch (`prod` until the Task 10
  cutover, then `main`) and **merging own PRs**
  (`gh pr merge --merge --delete-branch`) once PR checklist gates pass
  (tests pass, ruff check / ruff format --check / mypy clean,
  no secrets, AC met, docs updated).
- Running: git, gh, uv, uvx, cookiecutter, python 3.12+, pytest, ruff,
  mypy, pre-commit, docker build.
- Installing declared dependencies into the local environment (`uv sync`,
  `uv add` into the dev group only).
- Creating/editing/deleting any file inside the workspace needed for an
  accepted issue, including legacy template removal (`setup.sh`,
  `requirements/`, old `.env`, old GitHub template copies) once the
  corresponding issue is merged.
- Repo metadata edits on `mramitdas/CookiePyStarter` (description, topics,
  default branch, GitHub Pages from `/docs`) as specified by the approved
  design (docs/superpowers/specs/).
- Temporary network access to GitHub endpoints and package installs.

## Explicitly NOT pre-authorized (still require live user approval)

- `git push --force` (including to agent-created branches with history).
- Publishing, releasing, or deploying to any external host (including
  GitHub Releases/tags).
- Committing real secrets or editing `.env` with real credentials.
- Disabling or bypassing test/lint/type gates or Git Hooks.
- Operations on repos other than `mramitdas/CookiePyStarter` (including
  ecosystem PRs to cookiecutter/cookiecutter, awesome-python, etc.).
- Deleting branches other than agent-created merged branches
  (legacy `prod`/`dev`/`stag` are never deleted without live approval).

Rule: if an action is on the NOT list, stop and ask; everything else on the
standing list may proceed autonomously.
