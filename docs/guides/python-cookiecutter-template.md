# Python Cookiecutter Template: The Complete 2026 Guide

Cookiecutter is the de-facto tool for generating project scaffolds in Python,
and choosing the right **python cookiecutter template** is the difference
between a project that starts green and one you spend a weekend repairing.
This guide explains how to use a template, what the modern ones should give
you, and how [CookiePyStarter](https://github.com/mramitdas/CookiePyStarter)
fits in.

## What cookiecutter actually does

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) is a cross-platform
CLI that renders a template directory through [Jinja2](https://jinja.palletsprojects.com/)
while asking you a short series of questions defined in `cookiecutter.json`.
It supports hooks (scripts run before/after generation), choice variables,
and conditional files. Nothing about it is Python-specific — templates exist
for Rust, Terraform, docs — but Python is where it is most loved.

## Using a template in one command

```bash
uvx cookiecutter gh:mramitdas/CookiePyStarter
```

That command downloads the template, asks you its prompts, renders your
project, and — with CookiePyStarter — immediately runs lint, type check,
tests, installs dependencies with [uv](https://docs.astral.sh/uv/), installs
pre-commit hooks, and makes an initial git commit. If any of that fails,
generation stops loudly rather than handing you a broken project.

No global installs: `uvx` runs the tool in an ephemeral environment.

## What a *modern* python cookiecutter template must include

A template earns its keep by opinion, not volume. The 2026 baseline:

1. **`pyproject.toml` only.** PEP 621 metadata, no `requirements/*.txt`,
   no `setup.py`. Dependency groups (PEP 735) for dev extras.
2. **src layout.** `src/<package>/` keeps your tests honest (they import
   the *installed* package, never the working directory).
3. **ruff for lint + format.** One fast tool replacing flake8, black,
   isort, and autoflake.
4. **mypy (or pyright) strict.** Type checking configured before the first
   commit, not retrofitted.
5. **pytest with coverage.** And at least one real test — a template whose
   unit test file is empty teaches you nothing.
6. **pre-commit wired to the same tools.** CI and local checks should share
   one configuration.
7. **GitHub Actions from the first commit.** The matrix covers your chosen
   Python version.
8. **License handled properly.** Prompted, not hardcoded — and the template's
   own license should be permissive enough to reuse.

## How CookiePyStarter implements this

CookiePyStarter ships exactly ten prompts (name, package name, description,
author, email, GitHub username, license, Python version, Docker, docs) and
post-generation hook that:

- writes the license you chose (MIT, Apache-2.0, BSD-3-Clause, or CC0),
- removes the Docker/docs files you did not opt into,
- runs `uv sync`, `pre-commit install`, `git init` + initial commit,
- verifies `ruff`, `mypy --strict`, and `pytest` all pass.

Its own CI renders the template six ways (ubuntu + windows × three config
permutations) and runs full checks inside each render — so template changes
are never merged broken.

## Extending a template the right way

- Fork the template or drop additional prompts into `cookiecutter.json`.
- Add optional files and delete them in the post-generation hook
  (`remove_optional_paths`) when the option is off.
- Keep hook logic pure Python — it runs on Windows too.
- Wrap literal Jinja expressions inside generated GitHub Action files in a
  Jinja raw-tag block, or the GitHub Actions expressions will vanish.

## Get started

```bash
uvx cookiecutter gh:mramitdas/CookiePyStarter
```

Or browse the source at
<https://github.com/mramitdas/CookiePyStarter>.
