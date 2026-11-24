"""Encrypt/decrypt roundtrip for the message encryptor (needs `cryptography`)."""

import pytest
from conftest import load

pytest.importorskip("cryptography")
enc = load("03-data-security/exercises/file-encryptor/message_encryptor.py")


def _run(monkeypatch, func, answer):
    monkeypatch.setattr("builtins.input", lambda _prompt="": answer)
    func()


def test_roundtrip(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    enc.write_key()
    _run(monkeypatch, enc.encrypt_message, "secret hello")
    token = capsys.readouterr().out.strip().splitlines()[-1]
    assert "secret hello" not in token
    _run(monkeypatch, enc.decrypt_message, token)
    assert "secret hello" in capsys.readouterr().out


def test_wrong_key_fails(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    enc.write_key()
    _run(monkeypatch, enc.encrypt_message, "data")
    token = capsys.readouterr().out.strip().splitlines()[-1]
    enc.write_key()  # replaces key.key
    _run(monkeypatch, enc.decrypt_message, token)
    assert "Decryption failed" in capsys.readouterr().out


def test_missing_key_returns_none(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert enc.load_key() is None
