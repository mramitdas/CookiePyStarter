# uv + Cookiecutter: Dependency Management That Doesn't Hurt

Traditional Python projects still carry a stack of plain-text requirements
files, a hand-sourced virtual environment, and a wiki page explaining "
which interpreter version" — while
[uv](https://docs.astral.sh/uv/) deletes every step of that ritual. This
guide shows how **uv cookiecutter** setups work and why
[CookiePyStarter](https://github.com/mramitdas/CookiePyStarter) builds on uv
end to end.

## What uv replaces

| Old ritual | With uv |
|---|---|
| `python -m venv venv` + careful activation | `uv sync` creates `.venv` automatically |
| `pip install -r requirements/dev.txt` | `uv sync` (groups from `pyproject.toml`) |
| `pip freeze > requirements.txt` drift | `uv.lock` pins a reproducible graph |
| `pipx` for CLI tools | `uvx <tool>` caches and run on demand |
| Four config files for four tools | ruff + mypy config inside `pyproject.toml` |

uv is a single static binary, is fastest-in-class, understands standard
meta (`PEP 621`, `PEP 735`), and is now the default recommendation across
the Python tooling ecosystem.

## Where cookiecutter fits

A **uv cookiecutter** template means: after generation, the very next command
is `uv sync` — or better, the template has already run it. CookiePyStarter's
post-generation hook:

1. runs `uv sync` (creates `.venv`, installs runtime + dev groups),
2. runs `uvx`-style tooling for pre-commit and the check suite,
3. verifies `ruff`, `mypy`, `pytest` pass before generation ends.

```bash
uvx cookiecutter gh:mramitdas/CookiePyStarter
cd my_awesome_project
uv run pytest   # everything already installed and green
```

## The dependency-group pattern

CookiePyStarter generates:

```toml
[dependency-groups]
dev = ["mypy", "pre-commit", "pytest", "pytest-cov", "ruff"]
```

- `uv sync` installs the default group plus your project.
- Optional groups (e.g. `docs = ["mkdocs-material"]`) select with
  `uv sync --group docs` or `--extra docs` for extras.
- `uv.lock` is committed — every machine and CI run get identical deps.

## In CI

CookiePyStarter's generated GitHub Actions workflow (and the template's own
render-test matrix) use [`astral-sh/setup-uv`](https://github.com/astral-sh/setup-uv)
with cache enabled:

```yaml
- uses: astral-sh/setup-uv@v7
  with:
    enable-cache: true
- run: uv sync
- run: uv run pytest
```

Cold caches, warm keys: jobs finish in the time pip used to spend printing
"Collecting".

## Common gotchas

- **Forgetting to commit `uv.lock`** — reproducibility evaporates; commit it.
- **Mixing pip and uv installs** — pip will happily mutate `.venv` into an
  unsynced state; reinstall with `uv sync --reinstall`.
- **Global CLI installs** — prefer `uvx tool name` so versions stay pinned
  per invocation.
- **Renaming the default branch of a rendered project before the first
  push** — harmless, but CookiePyStarter already `git init`-ed `main` for you.

## Try it

```bash
uvx cookiecutter gh:mramitdas/CookiePyStarter
```

— a uv-native, src-layout, green-on-first-render Python project.
