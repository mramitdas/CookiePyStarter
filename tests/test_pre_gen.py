"""Tests for pre_gen_project package_name validation."""

from types import ModuleType

import pytest

from tests.conftest import load_hook


@pytest.fixture
def pre_gen() -> ModuleType:
    return load_hook("pre_gen_project")


def test_valid_names_pass(pre_gen: ModuleType) -> None:
    assert pre_gen.validate_package_name("my_pkg") == "my_pkg"
    assert pre_gen.validate_package_name("pkg2") == "pkg2"
    assert pre_gen.validate_package_name("_private") == "_private"


@pytest.mark.parametrize(
    "bad",
    ["My Class", "2pkg", "class", "", "my-pkg", "my.pkg"],
)
def test_invalid_names_exit_with_error(pre_gen: ModuleType, bad: str) -> None:
    with pytest.raises(SystemExit, match="not a valid Python package name"):
        pre_gen.validate_package_name(bad)
