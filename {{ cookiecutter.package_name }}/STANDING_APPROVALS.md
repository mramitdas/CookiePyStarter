# Agent Permissions — Standing Approvals

This file records approval the repository owner granted in-session so agents do
not need to wait for per-action confirmation. It is referenced by `AGENTS.md`
(Guardrails & Boundaries).

## Standing approvals (pre-authorized)

- Creating/deleting agent-created branches (`<type>/<issue#>-<slug>`).
- Commits, pushes to agent-created branches, and `origin` remote operations.
- Creating/updating/closing GitHub issues and comments.
- Creating PRs targeting the default branch (`main`) and **merging own PRs**
  (`gh pr merge --merge --delete-branch`) once PR checklist gates pass
  (tests pass, ruff check / ruff format --check / mypy clean,
  no secrets, AC met, docs updated).
- Running: git, gh, uv, uvx, python, pytest, ruff, mypy, pre-commit,
  docker build.
- Installing declared dependencies into the local environment (`uv sync`,
  `uv add` into the dev group only).
- Creating/editing/deleting any file inside the workspace needed for an
  accepted issue.
- Repo metadata edits on `{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}`
  (description, topics, default branch, GitHub Pages) as specified by an
  accepted issue.
- Temporary network access to GitHub endpoints and package installs.

## Explicitly NOT pre-authorized (still require live user approval)

- `git push --force` (including to agent-created branches with history).
- Publishing, releasing, or deploying to any external host (including
  GitHub Releases/tags).
- Committing real secrets or editing `.env` with real credentials.
- Disabling or bypassing test/lint/type gates or Git Hooks.
- Operations on repos other than `{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}`.
- Deleting branches other than agent-created merged branches.

Rule: if an action is on the NOT list, stop and ask; everything else on the
standing list may proceed autonomously.
