# {{ cookiecutter.project_name }}

**{{ cookiecutter.project_description }}**

## Install

```bash
uv sync
```

## Usage

```python
from {{ cookiecutter.package_name }} import add

add(2, 3)  # 5
```

## Develop

```bash
uv run pytest
uv run mkdocs serve
```
