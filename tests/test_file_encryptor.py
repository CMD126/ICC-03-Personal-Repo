import io
import os

import pytest
from conftest import ensure_tkinter, load

pytest.importorskip("cryptography")
from cryptography.fernet import Fernet, InvalidToken  # noqa: E402

ensure_tkinter()
lexcrypt = load("03-data-security/exercises/file-encryptor/lexcrypt_file_encryptor.py")


def test_derive_key_is_deterministic_per_salt():
    salt = b"s" * lexcrypt.SALT_SIZE
    key1, salt1 = lexcrypt.derive_key("correct horse", salt)
    key2, _ = lexcrypt.derive_key("correct horse", salt)
    other, _ = lexcrypt.derive_key("wrong horse", salt)
    assert key1 == key2 and salt1 == salt
    assert other != key1
    Fernet(key1)  # valid Fernet key


def test_derive_key_generates_random_salt():
    _, salt_a = lexcrypt.derive_key("pw")
    _, salt_b = lexcrypt.derive_key("pw")
    assert len(salt_a) == lexcrypt.SALT_SIZE
    assert salt_a != salt_b


def test_chunk_framing_roundtrip():
    buf = io.BytesIO()
    for chunk in (b"first", b"", b"x" * 1000):
        lexcrypt.write_chunk(buf, chunk)
    buf.seek(0)
    assert [lexcrypt.read_chunk(buf) for _ in range(3)] == [b"first", b"", b"x" * 1000]
    assert lexcrypt.read_chunk(buf) is None


@pytest.fixture
def small_chunks(monkeypatch):
    # Force several chunks so the framing is exercised with a small file.
    monkeypatch.setattr(lexcrypt, "CHUNK_SIZE", 64)


def test_encrypt_then_decrypt_file(tmp_path, small_chunks):
    fernet = Fernet(Fernet.generate_key())
    plain = tmp_path / "report.pdf"
    data = os.urandom(1000)
    plain.write_bytes(data)

    enc, out = tmp_path / "report.pdf.enc", tmp_path / "restored.pdf"
    lexcrypt.process_file(fernet, str(plain), str(enc), encrypt=True)
    assert data not in enc.read_bytes()
    lexcrypt.process_file(fernet, str(enc), str(out), encrypt=False)
    assert out.read_bytes() == data


def test_wrong_key_leaves_no_partial_output(tmp_path, small_chunks):
    plain = tmp_path / "a.txt"
    plain.write_bytes(b"secret" * 100)
    enc = tmp_path / "a.txt.enc"
    lexcrypt.process_file(Fernet(Fernet.generate_key()), str(plain), str(enc), encrypt=True)

    out = tmp_path / "a.txt.out"
    with pytest.raises(InvalidToken):
        lexcrypt.process_file(Fernet(Fernet.generate_key()), str(enc), str(out), encrypt=False)
    assert not out.exists()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["a.txt", "a.txt.enc"]


def test_wrong_key_keeps_existing_destination(tmp_path):
    plain = tmp_path / "a.txt"
    plain.write_bytes(b"data")
    enc = tmp_path / "a.txt.enc"
    lexcrypt.process_file(Fernet(Fernet.generate_key()), str(plain), str(enc), encrypt=True)
    with pytest.raises(InvalidToken):
        lexcrypt.process_file(Fernet(Fernet.generate_key()), str(enc), str(plain), encrypt=False)
    assert plain.read_bytes() == b"data"


def test_refuses_to_overwrite_source(tmp_path):
    plain = tmp_path / "a.txt"
    plain.write_bytes(b"precious")
    with pytest.raises(ValueError):
        lexcrypt.process_file(Fernet(Fernet.generate_key()), str(plain), str(plain), encrypt=True)
    assert plain.read_bytes() == b"precious"


def test_truncated_file_is_rejected(tmp_path):
    fernet = Fernet(Fernet.generate_key())
    plain, enc = tmp_path / "a", tmp_path / "a.enc"
    plain.write_bytes(b"hello world")
    lexcrypt.process_file(fernet, str(plain), str(enc), encrypt=True)
    enc.write_bytes(enc.read_bytes()[:-10])
    with pytest.raises(InvalidToken):
        lexcrypt.process_file(fernet, str(enc), str(tmp_path / "b"), encrypt=False)
