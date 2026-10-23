"""Tests for the load_hook test helper."""

import pytest

from tests.conftest import HOOKS_DIR, load_hook


def test_load_hook_raises_for_missing_module() -> None:
    with pytest.raises(FileNotFoundError, match="hook not found"):
        load_hook("does_not_exist")


def test_hooks_dir_is_known_path() -> None:
    assert HOOKS_DIR.name == "hooks"
