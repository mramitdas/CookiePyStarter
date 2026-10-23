# Modern Python Project Structure (2026)

"Where do my files go?" is the oldest question in Python, and the answer has
finally stabilized: **src layout, `pyproject.toml`, one lockfile, tools
configured in one place.** This guide explains what the modern Python
project structure looks like and why
[CookiePyStarter](https://github.com/mramitdas/CookiePyStarter) generates
exactly this shape.

## The reference layout

```
my_awesome_project/
├── src/
│   └── my_awesome_project/
│       ├── __init__.py        # __version__, public API re-exports
│       └── core.py            # real code, type-hinted
├── tests/
│   └── test_core.py           # imports the installed package
├── pyproject.toml             # metadata, deps, ruff/mypy/pytest config
├── uv.lock                    # reproducible dependency graph
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
├── README.md, CHANGELOG.md, LICENSE, CONTRIBUTING.md,
├── CODE_OF_CONDUCT.md, SECURITY.md
└── .gitignore
```

## Why src layout wins

With flat layout (package directory at the repo root), `import
my_awesome_project` resolves against your *working directory*. Consequences:

- Tests can pass locally against stale, not-yet-installed code.
- The famous "works on my machine" class of bugs: tests bypass packaging
  entirely.
- Accidental imports of top-level scripts.

With src layout, the package must be *built and installed* (or editable-
installed) so imports resolve inside `src/` — the same condition as
production, every time. `uv sync` handles the editable install; maturin and
hatchling both treat src layout as the default expectation.

## One file to configure them all

PEP 621 moved project metadata into `pyproject.toml`; in 2026 the linter
(ruff), type checker (mypy), and test runner (pytest) all read configuration
from the same TOML:

```toml
[tool.ruff]
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
strict = true
mypy_path = "src"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["--cov=my_awesome_package"]
```

No `setup.cfg`, no `tox.ini`, no `.flake8`, no tool sprawl.

## What belongs where

| Thing | Home |
|---|---|
| Runtime code | `src/<package>/` |
| Tests | `tests/` (top level, not inside the package) |
| Metadata + tool config | `pyproject.toml` |
| Long-form docs | `docs/` (mkdocs-material renders it) |
| CHANGELOG | `CHANGELOG.md`, Keep-a-Changelog format |
| Security policy | `SECURITY.md` (GitHub indexes it) |
| Contribution rules | `CONTRIBUTING.md` |

Files GitHub treats specially (SECURITY, SUPPORT, CODE_OF_CONDUCT,
FUNDING) surface in your Issues tab automatically — free process hygiene.

## Anti-patterns to retire

- **Empty `main.py` placeholders** — generate a real, tested module.
- **Committed `.env` files** — ignored by git; document env vars in README.
- **`scripts/` shell glue for setup** — a proper post-generation hook (or a
  Makefile/justfileTarget) beats unversioned bash.
- **GPL templates** — a template's license should not contaminate every
  project it creates; prefer Apache-2.0 or MIT for the template itself.
- **Vendoring transitive deps** into `requirements/dev.txt` — lockfiles did
  that job, better.

## Generate the 2026 layout in one command

```bash
uvx cookiecutter gh:mramitdas/CookiePyStarter
```

You get this structure — with Docker and mkdocs optionals — already green
under ruff, mypy --strict, and pytest.
