# Choosing a Python Boilerplate Generator

"python boilerplate generator" queries mostly hide two distinct jobs: create
a throwaway script fast, or start a project you will still be running next
year. This guide maps the tools: cookiecutter templates, uv's `init`
scaffold, pipenv/poetry's project commands — and where
[CookiePyStarter](https://github.com/mramitdas/CookiePyStarter) sits.

## The contenders

### 1. `uv init`
`uv init myproject` instantly gives you `pyproject.toml` + hello world.
Perfect for experiments and notebooks. It will not give you configured
ruff/mypy/pytest/pre-commit, a LICENSE, a CHANGELOG, CI, Docker, or docs —
by design it is minimal.

### 2. `poetry new` / `pipenv`
Framework-bound scaffolds less commonly needed in 2026 — poetry's project
commands and pipenv's workflows remain, but they lock your dependency
manager at birth.

### 3. Cookiecutter templates
Cookiecutter is the *generator* for opinionated starting points. Rules of
thumb when picking a template:

- **Freshness.** Check the last commit date; generated tooling rots.
- **Prompt economics.** Ten meaningful questions beat forty meaningless
  ones — you will press Enter through all forty anyway.
- **Tests for the template itself.** If the template repo's CI doesn't
  verify that *rendered output is green*, each merge gamble.
- **License hygiene.** The template should be permissive (MIT/Apache/BSD)
  and let *your project* choose its own license.
- **Post-generation behavior.** The best templates finish the job: install
  deps, install hooks, commit, and verify checks.

### 4. CookiePyStarter specifically
CookiePyStarter is a focused, general-purpose **python boilerplate
generator**: ten prompts, uv-native, src layout, ruff + mypy --strict +
pytest + pre-commit, GitHub Actions CI, license prompt
(MIT/Apache-2.0/BSD-3-Clause/CC0), optional Docker and mkdocs-material —
and rendered projects pass every check before the generator finishes:

```bash
uvx cookiecutter gh:mramitdas/CookiePyStarter
```

Its render-test matrix (ubuntu + windows × three config permutations) runs
the full check suite inside each generated project, so the template cannot
silently rot.

## Decision table

| You need | Use |
|---|---|
| Script/notebook scratch | `uv init` |
| Yearlong library/CLI with real tooling | **CookiePyStarter** |
| Django/Flask web app | cookiecutter-django (or framework docs) |
| Data-science analysis repo | locally-tailored cookiecutter with data extras |
| Distribution-ready docs + PyPI flow | CookiePyStarter, then add the release workflow |

## Start now

```bash
uvx cookiecutter gh:mramitdas/CookiePyStarter
cd my_awesome_project && uv run pytest   # already green
```

Further reading in this guide set: what this [python cookiecutter
template](python-cookiecutter-template.md) does, why the [modern Python
project structure](modern-python-project-structure.md) looks like this, and
how [uv + cookiecutter](uv-cookiecutter.md) collaborate.
