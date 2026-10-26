<p align="center">
  <img src="media/logo.png" width="150" alt="CookiePyStarter Logo">
</p>

<h1 align="center" style="border-bottom: none; margin-bottom: 0;">CookiePyStarter</h1>

<h2 align="center" style="border-bottom: none; font-weight: normal; margin-top: 4px;">Modern Python Cookiecutter Template</h2>

<p align="center">
  <strong>The modern, green-on-first-render Python project generator.</strong><br>
  uv · ruff · mypy · pytest · pre-commit · GitHub Actions · optional Docker & docs — in one command.
</p>

<p align="center">
  <a href="#quickstart-30-seconds">
    <img src="https://img.shields.io/badge/%F0%9F%9A%80_Quickstart-30_Seconds-0070f3?style=for-the-badge&logoColor=white" alt="Quickstart">
  </a>
  <a href="https://mramitdas.github.io/CookiePyStarter/">
    <img src="https://img.shields.io/badge/%F0%9F%93%96_Documentation-GitHub_Pages-2ea44f?style=for-the-badge&logoColor=white" alt="Docs">
  </a>
  <a href="https://github.com/mramitdas/CookiePyStarter/releases/tag/v1.0.0">
    <img src="https://img.shields.io/badge/%F0%9F%93%A6_Release-v1.0.0-8a2be2?style=for-the-badge&logoColor=white" alt="Release">
  </a>
</p>

<p align="center">
  <a href="https://github.com/mramitdas/CookiePyStarter/actions/workflows/render-test.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/mramitdas/CookiePyStarter/render-test.yml?label=render%20test" alt="Render Test">
  </a>
  <img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License Apache-2.0">
  <img src="https://img.shields.io/badge/python-3.10%7C3.11%7C3.12%7C3.13%7C3.14-blue.svg" alt="Python 3.10–3.14">
  <img src="https://img.shields.io/badge/code%20style-ruff-261230.svg" alt="Code style: ruff">
</p>

<p align="center">
  <img src="media/demo.gif" width="100%" alt="CookiePyStarter Terminal Demo">
</p>

CookiePyStarter is a [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
template that generates the Python project you always end up hand-rolling:
a [uv](https://docs.astral.sh/uv/)-managed, src-layout package wired with
[ruff](https://docs.astral.sh/ruff/), mypy, pytest, pre-commit, and GitHub
Actions CI — **and every generated project is green on first render** (the
generator itself runs lint, type check, and tests before it hands you the keys).

Works with the stock cookiecutter CLI — nothing else to install.

## Why Choose CookiePyStarter?

<table>
  <tr>
    <td width="50%">
      <h3>⚡ Green on First Render</h3>
      <p>Post-generation hook runs <code>uv sync</code>, <code>pre-commit install</code>, <code>ruff</code>, <code>mypy --strict</code>, and <code>pytest</code>. Your project passes every check before you even CD into it.</p>
    </td>
    <td width="50%">
      <h3>🚀 Instant uv Dependency Sync</h3>
      <p>Built native for <a href="https://docs.astral.sh/uv/">uv</a> with modern PEP 621 metadata and PEP 735 dependency groups. Zero legacy <code>requirements/*.txt</code> or <code>setup.sh</code> files.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🛡️ Strict Quality Gates</h3>
      <p>Shipped with <code>ruff</code> (lint + format), <code>mypy --strict</code> type checking, and non-vacuous <code>pytest</code> suite with coverage pre-configured in <code>pyproject.toml</code>.</p>
    </td>
    <td width="50%">
      <h3>📜 Selectable Licensing</h3>
      <p>Prompt-driven license generation: choose <strong>MIT</strong>, <strong>Apache-2.0</strong>, <strong>BSD-3-Clause</strong>, or <strong>CC0 (None)</strong>. The post-gen hook bakes author & year cleanly.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>🐳 Optional Docker & Docs</h3>
      <p>Opt-in during generation for a multi-stage <code>Dockerfile</code> and a complete <a href="https://squidfunk.github.io/mkdocs-material/">mkdocs-material</a> site scaffold.</p>
    </td>
    <td width="50%">
      <h3>🧪 Multi-OS CI Matrix</h3>
      <p>Every generated project includes a zero-config <code>.github/workflows/ci.yml</code> pipeline, while CookiePyStarter itself tests renders across Ubuntu & Windows matrix.</p>
    </td>
  </tr>
</table>

## Quickstart (30 seconds)

```bash
uvx cookiecutter gh:mramitdas/CookiePyStarter
```

Answer 10 short prompts (or press Enter for defaults) and get a project that
already passes `ruff check`, `ruff format --check`, `mypy --strict`, and
`pytest` — plus an initial git commit and pre-commit hooks installed.

Prefer pip? `pipx run cookiecutter gh:mramitdas/CookiePyStarter` works too.

## How It Works

```mermaid
flowchart LR
    A["10 Prompts"] --> B["Jinja2 Rendering"]
    B --> C["Post-Gen Hook"]
    C --> D["uv sync & git init"]
    D --> E["ruff & mypy & pytest"]
    E --> F["🎉 Green Project Ready"]
```

## What you get

```
my_awesome_project/
├── src/my_awesome_project/     # src-layout package (__version__ + utility + tests)
├── tests/                      # pytest suite with coverage (non-vacuous)
├── pyproject.toml              # PEP 621 metadata; ruff/mypy/pytest config inline
├── .pre-commit-config.yaml     # ruff + ruff-format + mypy hooks
├── .github/workflows/ci.yml    # GitHub Actions: lint + typecheck + tests
├── LICENSE                     # your choice: MIT / Apache-2.0 / BSD-3-Clause / CC0
├── README, CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY
├── AGENTS.md + STANDING_APPROVALS.md   # rules for AI coding agents
└── Dockerfile + mkdocs.yml     # only when you opted in
```

<p align="center">
  <img src="media/ci-green.png" width="100%" alt="GitHub Actions Render Matrix Passed">
</p>

Every dependency lives in `pyproject.toml` (PEP 735 dependency groups) — no
`requirements/` files, no `setup.sh`, no deserted tooling.

## The 10 prompts

| Prompt | Default | Choices |
|---|---|---|
| `project_name` | My Awesome Project | any |
| `package_name` | derived | valid Python identifier |
| `project_description` | A short description… | any |
| `author` | Your Name | any |
| `email` | you@example.com | any |
| `github_username` | your_github_username | any |
| `license` | MIT | MIT / Apache-2.0 / BSD-3-Clause / None (CC0) |
| `python_version` | 3.12 | 3.10 – 3.14 |
| `docker` | no | no / yes |
| `docs` | no | no / yes |

The package name is validated before generation: invalid input (spaces,
hyphens, keywords) aborts with a clear error, not a broken project.

## Why another Python cookiecutter template?

| | **CookiePyStarter** | cookiecutter-pypackage |
|---|---|---|
| Dependency management | **uv** (fast, PEP 735 groups) | pip / requirements |
| Lint + format | **ruff** (one tool) | flake8 + isort + separate config |
| Green-on-first-render | **yes** — generator runs the checks | no |
| Windows CI for the template itself | **yes** (render matrix) | partial |
| Generated project tests | real package imports + coverage | hello-world style |
| Docs engine option | mkdocs-material | mkdocs |
| License choice at generation | 4 options incl. CC0 | fixed |

This template targets the **modern Python project structure** (src layout,
PEP 621, single-source tool config) that the ecosystem has converged on in
2026. If you want a Django/Flask web scaffold, look at
[cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) —
CookiePyStarter is deliberately framework-agnostic.

## Documentation

Long-form guides live in [`docs/`](docs/) and are published on GitHub Pages:

- [Python cookiecutter template](https://mramitdas.github.io/CookiePyStarter/guides/python-cookiecutter-template.html) — how to use and extend
- [uv + cookiecutter](https://mramitdas.github.io/CookiePyStarter/guides/uv-cookiecutter.html) — dependency management that doesn't hurt
- [Modern Python project structure](https://mramitdas.github.io/CookiePyStarter/guides/modern-python-project-structure.html) — why src layout wins
- [Python boilerplate generator](https://mramitdas.github.io/CookiePyStarter/guides/python-boilerplate-generator.html) — picking the right starting point

## Requirements

- [uv](https://docs.astral.sh/uv/) (the post-generation hook uses it to sync
  dependencies, install pre-commit, and verify the project is green) and git.
  Without uv, generation stops with a friendly error.

## Community & support

- Questions → [Stack Overflow](https://stackoverflow.com/questions/tagged/cookiecutter), tag _cookiecutter_
- Bugs / ideas → [open an issue](https://github.com/mramitdas/CookiePyStarter/issues)
- Support the project → [GitHub Sponsors](https://github.com/sponsors/mramitdas) · [PayPal](https://paypal.me/mramitdas)

## Contributing

PRs welcome — see [CONTRIBUTING](.github/CONTRIBUTING.md) and the
[Code of Conduct](.github/CODE_OF_CONDUCT.md).

## License

This template is licensed under the [Apache License 2.0](LICENSE).
Generated projects choose their own license at generation time.
