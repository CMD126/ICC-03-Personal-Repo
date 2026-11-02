from conftest import load

log_analyzer = load("04-security-operations/exercises/log-analyzer/log_analyzer.py")

SAMPLE = """\
Mar 10 10:00:01 srv sshd[1]: Failed password for root from 10.0.0.5 port 22 ssh2
Mar 10 10:00:02 srv sshd[1]: Failed password for root from 10.0.0.5 port 22 ssh2
Mar 10 10:00:03 srv sshd[1]: Failed password for invalid user admin from 10.0.0.5 port 22 ssh2
Mar 10 10:00:04 srv sshd[1]: Failed password for root from 10.0.0.5 port 22 ssh2
Mar 10 10:00:05 srv sshd[1]: Failed password for root from 10.0.0.5 port 22 ssh2
Mar 10 10:00:06 srv sshd[1]: Failed password for bob from 192.168.1.20 port 22 ssh2
Mar 10 10:01:00 srv sshd[1]: Accepted password for bob from 192.168.1.20 port 22 ssh2
Mar 10 10:02:00 srv sshd[1]: Invalid user oracle from 10.0.0.9 port 22
"""


def test_parse_and_detect_brute_force(tmp_path):
    log = tmp_path / "auth.log"
    log.write_text(SAMPLE)

    failed, accepted, invalid = log_analyzer.parse_log(str(log))

    assert len(failed["10.0.0.5"]) == 5
    assert ("Mar 10 10:01:00", "bob", "192.168.1.20") in accepted
    assert invalid["oracle"] == 1

    brute = log_analyzer.detect_brute_force(failed)
    assert set(brute) == {"10.0.0.5"}


def test_missing_file_returns_none():
    assert log_analyzer.parse_log("/nonexistent/auth.log") == (None, None, None)
