import hashlib
import re

from conftest import load

ht = load("tools/hash-toolkit/hash_toolkit.py")


def identify(value):
    return [name for pattern, name in ht.HASH_SIGNATURES if re.match(pattern, value)]


def test_identifies_common_digests():
    assert "MD5 / MD4 / NTLM" in identify(hashlib.md5(b"x").hexdigest())
    assert "SHA-256" in identify(hashlib.sha256(b"x").hexdigest())
    assert "SHA-512" in identify(hashlib.sha512(b"x").hexdigest())


def test_identifies_bcrypt():
    sample = "$2b$12$" + "a" * 53
    assert "bcrypt" in identify(sample)


def test_hash_string_matches_hashlib():
    assert ht.hash_string("hello", hashlib.sha256) == hashlib.sha256(b"hello").hexdigest()


def test_hash_file_matches_hashlib(tmp_path):
    f = tmp_path / "data.bin"
    f.write_bytes(b"\x00" * 100_000)
    assert ht.hash_file(str(f), hashlib.sha256) == hashlib.sha256(b"\x00" * 100_000).hexdigest()
