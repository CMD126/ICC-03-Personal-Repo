"""Port scanner tests. They only talk to listeners on 127.0.0.1, never the network."""

import socket
import threading

import pytest
from conftest import load

scanner = load("08-penetration-testing/exercises/port-scanner/port_scanner.py")
scanner.TIMEOUT = 0.5


def _listener(greeting: bytes | None = None, reply: bytes | None = None):
    """Start a one-connection-at-a-time TCP server on a free local port."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(8)

    def serve():
        while True:
            try:
                conn, _ = srv.accept()
            except OSError:
                return
            with conn:
                if greeting:
                    conn.sendall(greeting)
                if reply:
                    conn.settimeout(2)
                    try:
                        if conn.recv(1024):
                            conn.sendall(reply)
                    except OSError:
                        pass

    threading.Thread(target=serve, daemon=True).start()
    return srv, srv.getsockname()[1]


def _closed_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_scan_port_open_and_closed():
    srv, port = _listener()
    try:
        assert scanner.scan_port("127.0.0.1", port) == {"port": port, "service": "Unknown"}
        assert scanner.scan_port("127.0.0.1", _closed_port()) is None
    finally:
        srv.close()


def test_scan_host_returns_only_open_ports_sorted():
    servers = [_listener() for _ in range(3)]
    try:
        open_ports = sorted(port for _, port in servers)
        result = scanner.scan_host("127.0.0.1", [_closed_port(), *reversed(open_ports)], max_threads=4)
        assert [r["port"] for r in result] == open_ports
    finally:
        for srv, _ in servers:
            srv.close()


def test_banner_from_service_that_speaks_first():
    srv, port = _listener(greeting=b"SSH-2.0-OpenSSH_9.6\r\n")
    try:
        assert scanner.grab_banner("127.0.0.1", port) == "SSH-2.0-OpenSSH_9.6"
    finally:
        srv.close()


def test_banner_from_http_service_after_probe():
    srv, port = _listener(reply=b"HTTP/1.0 200 OK\r\nServer: test\r\n\r\n")
    try:
        assert scanner.grab_banner("127.0.0.1", port) == "HTTP/1.0 200 OK"
    finally:
        srv.close()


def test_banner_on_closed_port_is_empty():
    assert scanner.grab_banner("127.0.0.1", _closed_port()) == ""


def test_common_ports_map_known_services():
    assert scanner.COMMON_PORTS[22] == "SSH"
    assert scanner.COMMON_PORTS[443] == "HTTPS"
    assert len(scanner.COMMON_PORTS) == 20


def test_parse_port_range_valid():
    assert scanner.parse_port_range("20", "25") == [20, 21, 22, 23, 24, 25]
    assert scanner.parse_port_range(" 80", "80 ") == [80]


@pytest.mark.parametrize(("start", "end"), [("0", "10"), ("10", "5"), ("1", "65536"), ("a", "10"), ("", "")])
def test_parse_port_range_invalid(start, end):
    with pytest.raises(ValueError):
        scanner.parse_port_range(start, end)
