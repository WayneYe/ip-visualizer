import pytest
import ipaddress
from generate_random_ips import generate_random_ip


def test_generate_random_ip_with_standard_network():
    """Test generating IP in a standard /24 network."""
    network = "192.168.1.0/24"
    ip = generate_random_ip(network)
    
    # Verify the IP is valid and within the network
    ip_obj = ipaddress.IPv4Address(ip)
    network_obj = ipaddress.ip_network(network, strict=False)
    
    assert ip_obj in network_obj.hosts() or ip_obj == network_obj.network_address or ip_obj == network_obj.broadcast_address


def test_generate_random_ip_with_slash_32_network():
    """Test generating IP in a /32 network (single IP)."""
    network = "10.0.0.1/32"
    ip = generate_random_ip(network)
    
    assert ip == "10.0.0.1"


def test_generate_random_ip_with_slash_31_network():
    """Test generating IP in a /31 network (only 2 IPs)."""
    network = "192.168.1.0/31"
    ip = generate_random_ip(network)
    
    # Should return one of the two possible IPs
    assert ip in ["192.168.1.0", "192.168.1.1"]


def test_generate_random_ip_with_large_network():
    """Test generating IP in a large network (class A)."""
    network = "10.0.0.0/8"
    ip = generate_random_ip(network)
    
    ip_obj = ipaddress.IPv4Address(ip)
    network_obj = ipaddress.ip_network(network, strict=False)
    
    assert ip_obj in network_obj.hosts() or ip_obj == network_obj.network_address or ip_obj == network_obj.broadcast_address


def test_generate_random_ip_with_small_network():
    """Test generating IP in a small network (/30)."""
    network = "192.168.1.0/30"
    ip = generate_random_ip(network)
    
    # Should be one of the two usable IPs (network and broadcast are excluded for /30)
    assert ip in ["192.168.1.1", "192.168.1.2"]


def test_generate_random_ip_with_non_strict_network():
    """Test generating IP with a non-strict network (host bits set)."""
    network = "192.168.1.100/24"  # 192.168.1.100 has host bits set for /24
    ip = generate_random_ip(network)
    
    ip_obj = ipaddress.IPv4Address(ip)
    network_obj = ipaddress.ip_network("192.168.1.0/24", strict=False)
    
    assert ip_obj in network_obj.hosts() or ip_obj == network_obj.network_address or ip_obj == network_obj.broadcast_address


if __name__ == "__main__":
    pytest.main(["-v"])

# To run the tests, use: python -m pytest test_generate_random_ips.py -v
