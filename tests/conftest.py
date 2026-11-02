"""Shared helpers for the test suite.

The tools live in folders with hyphens in their names (and are meant to be run
as standalone scripts), so they are not importable as normal packages. This
loads a script file as a module by path instead.
"""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load(relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def root() -> Path:
    return ROOT
