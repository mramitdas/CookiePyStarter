"""Validate the answered package_name before the template is rendered.

Runs at the root of the generated project with Jinja already substituted.
A non-zero exit aborts generation and removes the output directory.
"""

import keyword
import re

PACKAGE_NAME = "{{ cookiecutter.package_name }}"

_PATTERN = re.compile(r"^[_a-zA-Z][_a-zA-Z0-9]*$")


def validate_package_name(name: str) -> str:
    """Return name if it is a valid, non-keyword Python identifier."""
    if not _PATTERN.fullmatch(name) or keyword.iskeyword(name):
        raise SystemExit(
            f"ERROR: {name!r} is not a valid Python package name "
            "(snake_case identifier, not a keyword)."
        )
    return name


if __name__ == "__main__":
    validate_package_name(PACKAGE_NAME)
