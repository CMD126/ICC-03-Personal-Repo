"""
Safety tests for the ransomware simulator.

The simulator deletes originals after encrypting them, so the property that
matters most is that it can never act outside its sandbox. Every test points
SANDBOX and KEY_PATH at pytest's tmp_path.
"""

import os
from pathlib import Path

import pytest
from conftest import ensure_tkinter, load

pytest.importorskip("cryptography")
pytest.importorskip("PIL")

ensure_tkinter()
ransim = load("03-data-security/exercises/ransomware-simulator/ransomware_simulator.py")


@pytest.fixture
def lab(tmp_path, monkeypatch):
    sandbox = tmp_path / "lab_sandbox"
    sandbox.mkdir()
    outside = tmp_path / "real_data"
    outside.mkdir()
    monkeypatch.setattr(ransim, "SANDBOX", sandbox.resolve())
    monkeypatch.setattr(ransim, "KEY_PATH", tmp_path / "key.key")
    return sandbox, outside


def answer(monkeypatch, *replies):
    replies = iter(replies)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(replies))


# --- in_sandbox -------------------------------------------------------------

def test_in_sandbox_accepts_paths_inside(lab):
    sandbox, _ = lab
    assert ransim.in_sandbox(str(sandbox)) == sandbox.resolve()
    assert ransim.in_sandbox(str(sandbox / "a" / "b.txt")) == (sandbox / "a" / "b.txt").resolve()


def test_in_sandbox_refuses_outside_and_traversal(lab):
    sandbox, outside = lab
    assert ransim.in_sandbox(str(outside / "x.txt")) is None
    assert ransim.in_sandbox(str(sandbox / ".." / "real_data" / "x.txt")) is None
    assert ransim.in_sandbox("/etc/passwd") is None
    assert ransim.in_sandbox("~") is None


def test_in_sandbox_refuses_sibling_with_same_prefix(lab, tmp_path):
    # "lab_sandbox_evil" starts with the sandbox name but is not inside it.
    assert ransim.in_sandbox(str(tmp_path / "lab_sandbox_evil" / "x")) is None


def test_in_sandbox_refuses_symlink_pointing_outside(lab):
    sandbox, outside = lab
    (outside / "secret.txt").write_text("real data")
    (sandbox / "link.txt").symlink_to(outside / "secret.txt")
    (sandbox / "linkdir").symlink_to(outside, target_is_directory=True)
    assert ransim.in_sandbox(str(sandbox / "link.txt")) is None
    assert ransim.in_sandbox(str(sandbox / "linkdir")) is None


def test_in_sandbox_refuses_empty_input(lab, monkeypatch):
    sandbox, _ = lab
    monkeypatch.chdir(sandbox)  # "" would otherwise resolve to the cwd
    assert ransim.in_sandbox("") is None
    assert ransim.in_sandbox("   ") is None


# --- sandbox_problem ----------------------------------------------------------

def test_sandbox_problem_rejects_dangerous_locations():
    assert ransim.sandbox_problem(Path("/")) is not None
    assert ransim.sandbox_problem(Path.home()) is not None
    assert ransim.sandbox_problem(Path.home().parent) is not None
    assert ransim.sandbox_problem(ransim.BASE_DIR) is not None
    assert ransim.sandbox_problem(ransim.BASE_DIR.parent) is not None


def test_sandbox_problem_accepts_dedicated_folder(tmp_path):
    assert ransim.sandbox_problem(tmp_path / "lab_sandbox") is None
    assert ransim.sandbox_problem(ransim.BASE_DIR / "lab_sandbox") is None


# --- file and folder operations -----------------------------------------------

def test_encrypt_file_outside_sandbox_is_untouched(lab, monkeypatch):
    _, outside = lab
    target = outside / "important.docx"
    target.write_bytes(b"do not touch")
    answer(monkeypatch, str(target))
    ransim.encrypt_file()
    assert target.read_bytes() == b"do not touch"
    assert not (outside / "important.docx.enc").exists()


def test_encrypt_and_decrypt_file_roundtrip(lab, monkeypatch):
    sandbox, _ = lab
    target = sandbox / "notes.txt"
    target.write_bytes(b"lab data")

    answer(monkeypatch, str(target))
    ransim.encrypt_file()
    enc = sandbox / "notes.txt.enc"
    assert not target.exists() and enc.exists()
    assert b"lab data" not in enc.read_bytes()

    answer(monkeypatch, str(enc))
    ransim.decrypt_file()
    assert target.read_bytes() == b"lab data"
    assert not enc.exists()


def test_decrypt_file_does_not_overwrite_existing_file(lab, monkeypatch):
    sandbox, _ = lab
    target = sandbox / "a.txt"
    target.write_bytes(b"v1")
    answer(monkeypatch, str(target))
    ransim.encrypt_file()
    target.write_bytes(b"v2, newer")

    answer(monkeypatch, str(sandbox / "a.txt.enc"))
    ransim.decrypt_file()
    assert target.read_bytes() == b"v2, newer"
    assert (sandbox / "a.txt.enc").exists()


def test_folder_roundtrip_skips_symlinks(lab, monkeypatch):
    sandbox, outside = lab
    (sandbox / "sub").mkdir()
    files = {sandbox / "a.txt": b"A", sandbox / "sub" / "b.bin": os.urandom(64)}
    for path, data in files.items():
        path.write_bytes(data)
    real = outside / "real.txt"
    real.write_bytes(b"real data")
    (sandbox / "link.txt").symlink_to(real)
    (sandbox / "linkdir").symlink_to(outside, target_is_directory=True)

    answer(monkeypatch, str(sandbox))
    ransim.encrypt_folder()
    for path in files:
        assert not path.exists()
        assert path.with_suffix(path.suffix + ".enc").exists()
    assert (sandbox / "link.txt").is_symlink()
    assert not (sandbox / "link.txt.enc").exists()
    assert sorted(p.name for p in outside.iterdir()) == ["real.txt"]
    assert real.read_bytes() == b"real data"

    answer(monkeypatch, str(sandbox))
    ransim.decrypt_folder()
    for path, data in files.items():
        assert path.read_bytes() == data
    assert not list(sandbox.rglob("*.enc"))


def test_decrypt_folder_with_wrong_key_keeps_encrypted_files(lab, monkeypatch):
    sandbox, _ = lab
    (sandbox / "a.txt").write_bytes(b"A")
    answer(monkeypatch, str(sandbox))
    ransim.encrypt_folder()

    ransim.KEY_PATH.unlink()  # a new key will be generated
    answer(monkeypatch, str(sandbox))
    ransim.decrypt_folder()
    assert (sandbox / "a.txt.enc").exists()
    assert not (sandbox / "a.txt").exists()


def test_key_is_created_outside_the_sandbox(lab):
    sandbox, _ = lab
    ransim.if_key()
    assert ransim.KEY_PATH.exists()
    assert sandbox not in ransim.KEY_PATH.resolve().parents
