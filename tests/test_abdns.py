"""Pure logic in abdns: packet building and ranking (no network, no real DNS)."""

import struct

from conftest import load

abdns = load("tools/abdns/abdns_dns_benchmark.py")


def test_build_query_header_and_question():
    packet = abdns._build_query("example.com")
    _txid, flags, qd, an, ns, ar = struct.unpack(">HHHHHH", packet[:12])
    assert (flags, qd, an, ns, ar) == (0x0100, 1, 0, 0, 0)
    assert packet[12:] == b"\x07example\x03com\x00" + struct.pack(">HH", 1, 1)


def test_build_query_ignores_trailing_dot():
    assert abdns._build_query("example.com.")[12:] == abdns._build_query("example.com")[12:]


def test_benchmark_server_average_and_loss(monkeypatch):
    times = iter([10.0, float("inf"), 30.0, float("inf")])
    monkeypatch.setattr(abdns, "query_dns", lambda ip, domain: next(times))
    avg, loss = abdns.benchmark_server("1.2.3.4", ["a.com", "b.com"], count=2)
    assert avg == 20.0
    assert loss == 50.0


def test_benchmark_server_all_timeouts(monkeypatch):
    monkeypatch.setattr(abdns, "query_dns", lambda ip, domain: float("inf"))
    assert abdns.benchmark_server("1.2.3.4", ["a.com"], count=2) == (float("inf"), 100.0)


def test_analyse_dns_sorts_fastest_first_unreachable_last(monkeypatch, capsys):
    monkeypatch.setattr(abdns, "DNS_SERVERS", {"Slow": ("1.1.1.1", "1.0.0.1"),
                                               "Down": ("2.2.2.2", None),
                                               "Fast": ("3.3.3.3", None)})
    speeds = {"1.1.1.1": (50.0, 0.0), "2.2.2.2": (float("inf"), 100.0), "3.3.3.3": (5.0, 0.0)}
    monkeypatch.setattr(abdns, "benchmark_server", lambda ip, domains, verbose=False: speeds[ip])
    ranked = abdns.analyse_dns(["a.com"])
    assert [r[0] for r in ranked] == ["Fast", "Slow", "Down"]
    assert "UNREACHABLE" in capsys.readouterr().out
