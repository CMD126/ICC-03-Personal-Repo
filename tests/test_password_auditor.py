import hashlib

import pytest
from conftest import load

auditor = load("03-data-security/exercises/password-auditor/password_auditor.py")


@pytest.mark.parametrize(
    ("algorithm", "expected"),
    [
        ("md5", "5f4dcc3b5aa765d61d8327deb882cf99"),
        ("sha1", "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"),
        ("sha256", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"),
    ],
)
def test_known_digests_of_password(algorithm, expected):
    assert auditor.hash_password("password", algorithm) == (expected, None)


def test_salt_changes_the_digest_and_is_prepended():
    salt = b"\x00" * 16
    digest, returned_salt = auditor.hash_password("password", "sha256", salt)
    assert returned_salt == salt
    assert digest == hashlib.sha256(salt + b"password").hexdigest()
    assert digest != auditor.hash_password("password", "sha256")[0]


def test_unknown_algorithm_raises():
    with pytest.raises(ValueError):
        auditor.hash_password("password", "crc32")


@pytest.mark.parametrize("algorithm", ["md5", "sha1", "sha256", "sha512"])
def test_dictionary_attack_cracks_common_password(algorithm):
    target = auditor.hash_password("trustno1", algorithm)[0]
    assert auditor.dictionary_attack(target.upper() + "\n", algorithm) == "trustno1"


def test_dictionary_attack_misses_strong_password():
    target = auditor.hash_password("correct horse battery staple", "sha256")[0]
    assert auditor.dictionary_attack(target, "sha256") is None


def test_dictionary_attack_does_not_crack_salted_hash():
    target = auditor.hash_password("password", "md5", b"random-salt")[0]
    assert auditor.dictionary_attack(target, "md5") is None
