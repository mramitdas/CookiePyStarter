# {{ cookiecutter.project_name }}

**{{ cookiecutter.project_description }}**

[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.package_name }}/actions/workflows/ci.yml)

## Quickstart

```bash
uv sync                      # install deps (creates .venv)
uv run pytest                # run tests with coverage
uv run ruff check .          # lint
uv run mypy src/             # type-check
```

## Project layout

```
src/{{ cookiecutter.package_name }}/   # your package (src layout)
tests/               # pytest tests
pyproject.toml       # project metadata + tool config
```

## License

{{ cookiecutter.project_name }} is distributed under the terms of the
{% if cookiecutter.license == "None" %}CC0 1.0 license (public domain dedication).{% elif cookiecutter.license == "Apache-2.0" %}Apache License 2.0.{% elif cookiecutter.license == "BSD-3-Clause" %}BSD 3-Clause license.{% else %}MIT license.{% endif %} See `LICENSE` for details.
