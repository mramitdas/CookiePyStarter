"""Tests for post_gen_project file operations (no subprocess parts)."""

from pathlib import Path
from types import ModuleType

import pytest

from tests.conftest import load_hook


@pytest.fixture
def post_gen() -> ModuleType:
    return load_hook("post_gen_project")


def test_license_map_covers_exactly_the_four_choices(post_gen: ModuleType) -> None:
    assert set(post_gen.LICENSE_MAP) == {
        "MIT",
        "Apache-2.0",
        "BSD-3-Clause",
        "None",
    }


@pytest.mark.parametrize(
    ("choice", "marker"),
    [
        ("MIT", "MIT License"),
        ("Apache-2.0", "Apache License"),
        ("BSD-3-Clause", "Redistribution and use"),
        ("None", "CC0 1.0 Universal"),
    ],
)
def test_write_license_emits_file_and_removes_templates(
    post_gen: ModuleType, tmp_path: Path, choice: str, marker: str
) -> None:
    templates = tmp_path / ".license_templates"
    templates.mkdir()
    # Cookiecutter has already Jinja-rendered author into the file by hook time.
    (templates / post_gen.LICENSE_MAP[choice]).write_text(
        f"{marker} __YEAR__ Ada Lovelace\n", encoding="utf-8"
    )
    (templates / "extra.txt").write_text("x", encoding="utf-8")

    post_gen.write_license(choice, "2026", tmp_path)

    text = (tmp_path / "LICENSE").read_text(encoding="utf-8")
    assert marker in text
    assert "2026" in text
    assert "Ada Lovelace" in text
    assert not templates.exists()


def test_write_license_substitutes_year_placeholder(
    post_gen: ModuleType, tmp_path: Path
) -> None:
    templates = tmp_path / ".license_templates"
    templates.mkdir()
    (templates / "MIT.txt").write_text(
        "Copyright (c) __YEAR__ Author\n", encoding="utf-8"
    )

    post_gen.write_license("MIT", "1999", tmp_path)

    licensed = (tmp_path / "LICENSE").read_text(encoding="utf-8")
    assert "Copyright (c) 1999 Author" in licensed


def test_write_license_unknown_choice_raises(
    post_gen: ModuleType, tmp_path: Path
) -> None:
    with pytest.raises(KeyError):
        post_gen.write_license("WTFPL", "2026", tmp_path)


def test_remove_optional_paths_deletes_files_and_dirs(
    post_gen: ModuleType, tmp_path: Path
) -> None:
    (tmp_path / "Dockerfile").write_text("x", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text("x", encoding="utf-8")
    (tmp_path / "keep.txt").write_text("keep", encoding="utf-8")

    post_gen.remove_optional_paths(["Dockerfile", "docs", "missing.txt"], tmp_path)

    assert not (tmp_path / "Dockerfile").exists()
    assert not (tmp_path / "docs").exists()
    assert (tmp_path / "keep.txt").exists()
