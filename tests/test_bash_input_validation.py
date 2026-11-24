"""
Input validation in the Bash tools.

Each script is sourced (its menu only starts when it is executed) and the
validator is called with a single argument, so these tests run no network or
system commands. The bad inputs are the ones that matter: option injection
("-..." reaching nmap/apt/dig), arithmetic command substitution, and URL or
path characters.
"""

import shutil
import subprocess
import sys

import pytest
from conftest import ROOT

pytestmark = [
    pytest.mark.skipif(shutil.which("bash") is None, reason="bash not installed"),
    # On Windows "bash" is often the WSL launcher, which cannot take Windows paths
    pytest.mark.skipif(sys.platform == "win32", reason="bash on Windows (WSL) cannot source scripts by Windows path"),
]

NETDIAG = "tools/network-tool/net_diagnostic_tool.sh"
NMATRIX = "tools/nmatrix/nmatrix_nmap_scanner.sh"
RECON = "tools/recon-tool/recon_tool.sh"
SYSCRIPT = "tools/syscript/syscript_sysadmin.sh"


def bash(script: str, snippet: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        # $0 stays "bash" so the script's "executed, not sourced" guard holds
        ["bash", "-c", f'source "$1" >/dev/null 2>&1; shift; {snippet}', "bash", str(ROOT / script), *args],
        stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10,
    )


def accepts(script: str, func: str, *args: str) -> bool:
    return bash(script, f'{func} "$@"', *args).returncode == 0


GOOD_HOSTS = ["8.8.8.8", "localhost", "example.com", "sub-domain.example.co.uk", "2001:db8::1", "my_host"]
BAD_HOSTS = [
    "", "-oN/tmp/x", "--script=/tmp/evil.nse", "example.com;id", "$(id)", "a b",
    "host/../../etc", "example.com?x=1", "-", "a" * 254,
]


@pytest.mark.parametrize("script", [NETDIAG, NMATRIX])
@pytest.mark.parametrize("host", GOOD_HOSTS)
def test_valid_hosts_are_accepted(script, host):
    assert accepts(script, "is_valid_host", host)


@pytest.mark.parametrize("script", [NETDIAG, NMATRIX])
@pytest.mark.parametrize("host", BAD_HOSTS)
def test_injection_attempts_in_host_are_rejected(script, host):
    assert not accepts(script, "is_valid_host", host)


@pytest.mark.parametrize("script", [NETDIAG, NMATRIX])
def test_network_validation(script):
    for good in ["192.168.1.0/24", "10.0.0.1", "fe80::/64"]:
        assert accepts(script, "is_valid_network", good), good
    for bad in ["-sV", "192.168.1.0/24 --script vuln", "net;id", ""]:
        assert not accepts(script, "is_valid_network", bad), bad


@pytest.mark.parametrize(
    ("value", "ok"),
    [("1", True), ("20", True), ("500", True), ("007", True), ("0", False), ("501", False),
     ("", False), ("-5", False), ("1.5", False), ("a[$(touch /tmp/pwned)]", False), ("1e3", False)],
)
def test_int_in_range(value, ok):
    assert accepts(NETDIAG, "is_int_in_range", value, "1", "500") is ok


def test_arithmetic_injection_does_not_execute(tmp_path):
    marker = tmp_path / "pwned"
    payload = f"a[$(touch {marker})]"
    bash(NETDIAG, 'is_int_in_range "$1" 1 500', payload)
    assert not marker.exists()


@pytest.mark.parametrize(
    ("spec", "ok"),
    [("80", True), ("1-1000", True), ("22,80,443", True), ("1-100,443,8000-8100", True),
     ("0", False), ("65536", False), ("100-1", False), ("80,", False), (",80", False),
     ("-p-", False), ("80 --script vuln", False), ("", False)],
)
def test_port_spec(spec, ok):
    assert accepts(NETDIAG, "is_valid_port_spec", spec) is ok


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("Example.COM", "example.com"), ("https://example.com/path?q=1", "example.com"),
     ("http://example.com:8080/", "example.com"), ("10.0.0.1:443", "10.0.0.1"),
     ("2001:db8::1", "2001:db8::1")],
)
def test_recon_normalize_target(raw, expected):
    assert bash(RECON, 'normalize_target "$1"', raw).stdout == expected


@pytest.mark.parametrize("target", ["example.com", "10.0.0.1", "2001:db8::1"])
def test_recon_accepts_targets(target):
    assert accepts(RECON, "is_valid_target", target)


@pytest.mark.parametrize("target", ["-h", "example.com&fields=x", "..", "../../tmp/x", "a b", "$(id)"])
def test_recon_rejects_targets(target):
    assert not accepts(RECON, "is_valid_target", target)


@pytest.mark.parametrize(("name", "ok"), [
    ("curl", True), ("libc6:amd64", True), ("curl=8.5.0-2", True), ("g++", True),
    ("-oAPT::Update::Pre-Invoke::=id", False), ("curl -y", False), ("Curl", False), ("", False),
])
def test_syscript_package_names(name, ok):
    assert accepts(SYSCRIPT, "is_valid_pkg", name) is ok


@pytest.mark.parametrize(("name", "ok"), [
    ("ssh", True), ("nginx.service", True), ("getty@tty1.service", True),
    ("--now", False), ("ssh; reboot", False), ("", False),
])
def test_syscript_unit_names(name, ok):
    assert accepts(SYSCRIPT, "is_valid_unit", name) is ok


@pytest.mark.parametrize("script", [NETDIAG, NMATRIX, RECON, SYSCRIPT])
def test_sourcing_does_not_start_the_menu(script):
    result = bash(script, "echo sourced-ok")
    assert result.returncode == 0
    assert result.stdout.strip() == "sourced-ok"
