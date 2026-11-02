from conftest import load

ioc = load("06-threat-hunting/exercises/ioc-scanner/ioc_scanner.py")


def make_feed(tmp_path):
    feed = tmp_path / "iocs.txt"
    feed.write_text(
        "# test feed\n"
        "ip:203.0.113.66:HIGH:Known C2 server\n"
        "domain:evil-updates.xyz:CRITICAL:Malware dropper\n"
        "hash:44d88612fea8a8f36de82e1278abb02f:CRITICAL:EICAR test file\n"
    )
    return ioc.load_iocs(str(feed))


def test_scan_text_finds_each_ioc_type(tmp_path):
    iocs = make_feed(tmp_path)
    line = (
        "conn from 203.0.113.66 to evil-updates.xyz, "
        "dropped file md5=44d88612fea8a8f36de82e1278abb02f"
    )
    hits = ioc.scan_text(line, iocs, source="test.log")
    assert {h["type"] for h in hits} == {"IP", "Domain", "Hash"}


def test_clean_text_has_no_hits(tmp_path):
    iocs = make_feed(tmp_path)
    assert ioc.scan_text("GET /index.html from 198.51.100.1 example.com", iocs) == []


def test_bundled_sample_feed_loads():
    iocs = ioc.load_iocs()
    assert sum(len(v) for v in iocs.values()) > 0
