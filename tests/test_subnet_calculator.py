import ipaddress
import time

import pytest
from conftest import load

subnet = load("01-networking-and-sysadmin/exercises/subnet-calculator/subnet_calculator.py")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("192.168.1.0/24", "192.168.1.0/24"),
        ("192.168.1.77/24", "192.168.1.0/24"),
        ("10.0.0.0 255.255.255.0", "10.0.0.0/24"),
        ("  172.16.5.4/12 ", "172.16.0.0/12"),
    ],
)
def test_parse_network_accepts_cidr_and_mask(raw, expected):
    assert str(subnet.parse_network(raw)) == expected


@pytest.mark.parametrize("raw", ["", "300.1.1.1/24", "10.0.0.0/33", "10.0.0.0 255.0.255.0", "a b c"])
def test_parse_network_rejects_bad_input(raw):
    with pytest.raises(ValueError):
        subnet.parse_network(raw)


@pytest.mark.parametrize(
    ("cidr", "first", "last", "usable"),
    [
        ("192.168.1.0/24", "192.168.1.1", "192.168.1.254", 254),
        ("10.0.0.0/30", "10.0.0.1", "10.0.0.2", 2),
        ("10.0.0.0/31", "10.0.0.0", "10.0.0.1", 2),
        ("10.0.0.5/32", "10.0.0.5", "10.0.0.5", 1),
    ],
)
def test_host_range_matches_ipaddress(cidr, first, last, usable):
    net = ipaddress.IPv4Network(cidr)
    got = subnet.host_range(net)
    assert (str(got[0]), str(got[1]), got[2]) == (first, last, usable)
    hosts = list(net.hosts())
    assert (got[0], got[1], got[2]) == (hosts[0], hosts[-1], len(hosts))


def test_host_range_is_instant_for_huge_networks():
    # Listing every host of 0.0.0.0/0 used to hang the tool.
    start = time.perf_counter()
    first, last, usable = subnet.host_range(ipaddress.IPv4Network("0.0.0.0/0"))
    assert time.perf_counter() - start < 0.1
    assert (str(first), str(last), usable) == ("0.0.0.1", "255.255.255.254", 2**32 - 2)


def test_split_network_into_four():
    prefix, subnets = subnet.split_network(ipaddress.IPv4Network("192.168.1.0/24"), 4)
    assert prefix == 26
    assert [str(s) for s in subnets] == [
        "192.168.1.0/26", "192.168.1.64/26", "192.168.1.128/26", "192.168.1.192/26",
    ]


def test_split_network_rounds_up_to_power_of_two():
    prefix, subnets = subnet.split_network(ipaddress.IPv4Network("10.0.0.0/24"), 3)
    assert prefix == 26
    assert len(subnets) == 3


def test_split_network_refuses_when_too_small():
    with pytest.raises(ValueError):
        subnet.split_network(ipaddress.IPv4Network("10.0.0.0/29"), 4)
    with pytest.raises(ValueError):
        subnet.split_network(ipaddress.IPv4Network("10.0.0.0/24"), 1)


@pytest.mark.parametrize(
    ("ip", "cls"),
    [("10.1.2.3", "A"), ("127.0.0.1", "A"), ("172.16.0.1", "B"), ("192.168.0.1", "C"),
     ("224.0.0.1", "D (Multicast)"), ("250.0.0.1", "E (Reserved)")],
)
def test_ip_class(ip, cls):
    assert subnet.ip_class(ipaddress.IPv4Address(ip))[0] == cls
