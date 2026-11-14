"""Shared helpers for the test suite.

The tools live in folders with hyphens in their names (and are meant to be run
as standalone scripts), so they are not importable as normal packages. This
loads a script file as a module by path instead.
"""

import importlib.util
import sys
import types
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load(relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ensure_tkinter():
    """
    Make `import tkinter` work for GUI scripts whose logic we test without a GUI.

    Minimal Python installs and CI containers often ship without Tk. In that case
    a stub package is registered; the tests never create a window, so the stub
    only has to satisfy the imports and names used at module level.
    """
    try:
        import tkinter  # noqa: F401
        return
    except ImportError:
        pass
    tk = types.ModuleType("tkinter")
    tk.__getattr__ = lambda name: mock.MagicMock(name=f"tkinter.{name}")
    sys.modules["tkinter"] = tk
    for sub in ("filedialog", "messagebox", "simpledialog", "ttk"):
        module = mock.MagicMock(name=f"tkinter.{sub}")
        sys.modules[f"tkinter.{sub}"] = module
        setattr(tk, sub, module)


@pytest.fixture
def root() -> Path:
    return ROOT
