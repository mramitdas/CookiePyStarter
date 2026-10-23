# Design: CookiePyStarter Rebuild — Modern Python Cookiecutter Template

**Status:** Approved (2026-10-23)

## Intent
Turn CookiePyStarter from a pre-product template (empty files, pip/venv
tooling, GPL-3.0, broken links) into the definitive modern-Python starter:
pure OSS, sponsor-funded, brand kept, SEO via keyword-stuffed metadata +
docs site. Success = generated projects are green on first render, and the
repo surfaces for "python cookiecutter" searches.

## Goals
- `uvx cookiecutter gh:mramitdas/CookiePyStarter` → project that passes
  lint, typecheck, and tests immediately.
- Toolchain: uv, PEP 621 `pyproject.toml`, src layout, ruff (lint+format),
  pytest+coverage, mypy, pre-commit, GitHub Actions.
- ≤10 prompts; post-gen hook (Python, Windows-safe): uv sync, pre-commit
  install, git init + initial commit, verify green.
- Repo relicensed GPL-3.0 → Apache-2.0; generated projects get a license
  prompt (MIT default; Apache-2.0, BSD-3-Clause, None/CC0).
- Template-repo CI renders the template in multiple permutations and tests
  the output (quality moat).
- SEO: keyword-stuffed GitHub description + topics (`cookiecutter`,
  `cookiecutter-template`, `python`, `template`, `boilerplate`, `uv`,
  `ruff`, `pytest`, `pre-commit`, `docker`, `github-actions`); README H1
  "CookiePyStarter — Modern Python Cookiecutter Template" with 30s
  quickstart + comparison table vs cookiecutter-pypackage; 4 long-tail
  guides on GitHub Pages (`/docs`, this repo); ecosystem listing PRs
  (deferred to user — standing approvals do not cover other repos).
- Fix all known bugs (branch-slash links, env/venv, app/main.py refs,
  committed .env) by replacing the affected files wholesale; collapse
  prod/dev/stag → `main`.

## Non-goals
No CLI product / paid tiers / hosted service. No multi-type mega-template.
No web-framework presets. No changes to cookiecutter itself (works on
≥2.2, verified against 2.7.1). No non-GitHub CI in v1.

## Anti-goals
Generated project not green on first render · prompt wall · GPL left in
place · marketing README without working quickstart · stale pinned tools.

## Constraints
Standard cookiecutter layout; Python 3.10–3.14 for generated projects;
Python 3.12+ for repo dev; cross-platform hooks (pure Python); docs on
GitHub Pages from `/docs` (user decision, no custom domain in v1).

## Approaches (decided)
Smart template + post-gen hook — chosen over kitchen-sink prompts
(rejected: friction/quality dilution) and CLI-wrapper (rejected: wrong
model). Keep brand + keyword technique — chosen over rename and rebrand.

## Prompts (10)
`project_name`, `package_name` (derived default; directory name),
`project_description`, `author`, `email`, `github_username`, `license`
(MIT default / Apache-2.0 / BSD-3-Clause / None→CC0), `python_version`
(3.12 default; 3.10–3.14), `docker` (no default), `docs` (no default)

## Hook design (docs-verified 2026-10-23)
- `hooks/pre_gen_project.py` validates the answered `package_name`
  (valid identifier, not a keyword). `pre_prompt` runs before questions
  and cannot validate answers — earlier plan to use it was corrected.
- `hooks/post_gen_project.py`: write LICENSE from `.license_templates/`;
  remove docker/docs files when not selected; `uv sync`;
  `uv run pre-commit install`; `git init` + initial commit using
  `-c user.name/-c user.email` from prompts; run ruff/mypy/pytest; any
  failure exits non-zero (generation halts loudly). Friendly error if
  `uv` or `git` is missing.

## Builder calls (approved set)
1. Build backend: hatchling. 2. Type checker: mypy. 3. Generated
`docs=y` → mkdocs-material, default no. 4. Render-test matrix includes
windows-latest; permutations: default / docker=yes / license=Apache-2.0.
5. Sample code: `__version__` + `add()` utility + matching test.
6. License "None" emits CC0-1.0. 7. Hook is pure Python; friendly error
if uv/git missing. 8. Old prod/dev/stag branches kept, archived later by
owner — nothing deleted.

## Left to builder
Ruff rule set, mypy strictness details, workflow YAML, hook code, copy,
badge URLs, dep pin strategy, mkdocs config, CHANGELOG contents.
