"""Finalize the generated project and verify it is green.

Runs at the root of the generated project after rendering. Any failure
exits non-zero so cookiecutter halts loudly (and removes the output).
"""

import shutil
import subprocess
from datetime import date
from pathlib import Path

LICENSE_MAP: dict[str, str] = {
    "MIT": "MIT.txt",
    "Apache-2.0": "APACHE.txt",
    "BSD-3-Clause": "BSD3.txt",
    "None": "CC0.txt",
}

LICENSE_CHOICE = "{{ cookiecutter.license }}"
DOCKER = "{{ cookiecutter.docker }}"
DOCS = "{{ cookiecutter.docs }}"
AUTHOR = "{{ cookiecutter.author }}"
EMAIL = "{{ cookiecutter.email }}"


def write_license(license_choice: str, year: str, cwd: Path) -> None:
    """Write LICENSE from .license_templates/<mapped> and remove the dir.

    Author/copyright holder is already Jinja-rendered into the template
    files by cookiecutter before this hook runs; only __YEAR__ is left
    for runtime substitution.
    """
    template_name = LICENSE_MAP[license_choice]
    template_path = cwd / ".license_templates" / template_name
    text = template_path.read_text(encoding="utf-8")
    text = text.replace("__YEAR__", year)
    (cwd / "LICENSE").write_text(text, encoding="utf-8")
    shutil.rmtree(cwd / ".license_templates")


def remove_optional_paths(paths: list[str], cwd: Path) -> None:
    """Delete files or directories from cwd if they exist."""
    for name in paths:
        target = cwd / name
        if target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)


def run(*args: str) -> None:
    """Run a command, exiting loudly with a friendly message on failure."""
    try:
        subprocess.run(args, check=True)
    except FileNotFoundError:
        tool = args[0]
        print(
            f"ERROR: {tool!r} is required to finish setup but was not found "
            "on PATH. Install it (https://docs.astral.sh/uv/ for uv) and "
            "re-run cookiecutter."
        )
        raise SystemExit(1) from None
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: setup command failed: {' '.join(args)} (exit {exc.returncode})")
        raise SystemExit(1) from None


def run_setup(author: str, email: str) -> None:
    """Install deps, hooks, git-init, and verify lint/type/tests pass."""
    run("git", "init")
    run("uv", "sync")
    run("uv", "run", "pre-commit", "install")
    run("git", "add", "-A")
    run(
        "git",
        "-c",
        f"user.name={author}",
        "-c",
        f"user.email={email}",
        "commit",
        "-m",
        "Initial commit from CookiePyStarter",
    )
    run("uv", "run", "ruff", "check", ".")
    run("uv", "run", "ruff", "format", "--check", ".")
    run("uv", "run", "mypy", "src/")
    run("uv", "run", "pytest")


if __name__ == "__main__":
    cwd = Path.cwd()
    write_license(LICENSE_CHOICE, str(date.today().year), cwd)
    optional_paths: list[str] = []
    if DOCKER != "yes":
        optional_paths += ["Dockerfile", ".dockerignore"]
    if DOCS != "yes":
        optional_paths += ["mkdocs.yml", "docs"]
    remove_optional_paths(optional_paths, cwd)
    run_setup(AUTHOR, EMAIL)
