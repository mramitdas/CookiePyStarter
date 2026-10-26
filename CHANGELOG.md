# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Generated projects now include `AGENTS.md` and `STANDING_APPROVALS.md`:
  agent rules (stack, commands, layout, guardrails) and standing approvals,
  rendered per project.
- Render-test CI asserts the agent governance files render without leftover
  Jinja.

## [1.0.0] - 2026-10-23

The 2026 rebuild: CookiePyStarter as a modern Python cookiecutter template.

### Added

- Ten-prompt cookiecutter template producing a src-layout package with
  `__version__`, an `add()` utility, and matching tests.
- `pyproject.toml` generation with PEP 621 metadata, hatchling backend, and
  inline ruff/mypy/pytest configuration.
- License prompt: MIT (default), Apache-2.0, BSD-3-Clause, or CC0-1.0,
  written by the post-generation hook.
- Docker option: multi-stage Dockerfile + .dockerignore.
- Docs option: mkdocs-material site scaffold.
- GitHub Actions CI in generated projects (lint, format, mypy, pytest).
- Post-generation hook that installs dependencies via uv, installs pre-commit,
  creates the initial git commit, and verifies the project is green.
- Pre-generation validation of `package_name` (identifier, not keyword).
- Template render-test CI matrix (ubuntu + windows × default/docker/apache).
- Repo dev tooling: ruff, mypy (strict), pytest, pre-commit.
- SEO-focused README and four long-form guides (GitHub Pages).

### Removed

- Legacy venv + pip + `requirements/*.txt` setup, `setup.sh`, empty
  `src/main.py`, flake8-based CI, GPL-3.0 license (now Apache-2.0),
  hardcoded CC0 output license, committed `.env` placeholder.
