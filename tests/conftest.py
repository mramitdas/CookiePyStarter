"""Shared fixtures for CookiePyStarter template tests."""

import importlib.util
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOKS_DIR = REPO_ROOT / "hooks"


def load_hook(name: str) -> ModuleType:
    """Import a hook script from hooks/ by module name for unit testing."""
    path = HOOKS_DIR / f"{name}.py"
    if not path.exists():
        raise FileNotFoundError(f"hook not found: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load hook: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
