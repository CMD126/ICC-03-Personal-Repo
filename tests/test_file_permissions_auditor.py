import os
import stat

import pytest
from conftest import load

perms = load("00-foundations/exercises/file-permissions-auditor/file_permissions_auditor.py")


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        (0o777, "rwxrwxrwx"),
        (0o755, "rwxr-xr-x"),
        (0o644, "rw-r--r--"),
        (0o600, "rw-------"),
        (0o4755, "rwsr-xr-x"),
        (0o4644, "rwSr--r--"),
        (0o2755, "rwxr-sr-x"),
        (0o1777, "rwxrwxrwt"),
        (0o1776, "rwxrwxrwT"),
    ],
)
def test_format_permissions_matches_ls(mode, expected):
    assert perms.format_permissions(mode) == expected
    # Cross-check against the standard library (it adds the file type char).
    assert stat.filemode(stat.S_IFREG | mode)[1:] == expected


def _make(path, mode):
    path.write_text("x")
    os.chmod(path, mode)
    return str(path)


def test_world_writable_finds_files_and_ignores_symlinks(tmp_path):
    bad = _make(tmp_path / "open.txt", 0o666)
    _make(tmp_path / "ok.txt", 0o644)
    (tmp_path / "link").symlink_to(tmp_path / "ok.txt")  # symlinks always look 0777
    found = [f for f, _ in perms.world_writable_files(str(tmp_path))]
    assert found == [bad]


def test_hidden_directories_are_skipped(tmp_path):
    hidden = tmp_path / ".git"
    hidden.mkdir()
    _make(hidden / "open.txt", 0o666)
    assert perms.world_writable_files(str(tmp_path)) == []


def test_suid_and_sgid_detection(tmp_path):
    suid = _make(tmp_path / "suid_bin", 0o4755)
    sgid = _make(tmp_path / "sgid_bin", 0o2755)
    _make(tmp_path / "plain_bin", 0o755)
    if not (os.stat(suid).st_mode & stat.S_ISUID and os.stat(sgid).st_mode & stat.S_ISGID):
        pytest.skip("filesystem cleared the SUID or SGID bit")
    suid_found, sgid_found = perms.suid_sgid_files(str(tmp_path))
    assert [f for f, _ in suid_found] == [suid]
    assert [f for f, _ in sgid_found] == [sgid]
