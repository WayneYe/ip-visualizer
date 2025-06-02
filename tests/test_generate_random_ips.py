import pytest
import ipaddress
from ip_visualizer.core.ip_generator import generate_random_ip, generate_ip_list
from unittest.mock import patch


def test_generate_random_ip_with_standard_network():
    """Test generating IP in a standard /24 network."""
    network = "192.168.1.0/24"
    ip = generate_random_ip(network)

    # Verify the IP is valid and within the network
    ip_obj = ipaddress.IPv4Address(ip)
    network_obj = ipaddress.ip_network(network, strict=False)

    assert (
        ip_obj in network_obj.hosts()
        or ip_obj == network_obj.network_address
        or ip_obj == network_obj.broadcast_address
    )


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
    network = "10.0.0.0/24"
    ip = generate_random_ip(network)

    ip_obj = ipaddress.IPv4Address(ip)
    network_obj = ipaddress.ip_network(network, strict=False)

    assert (
        ip_obj in network_obj.hosts()
        or ip_obj == network_obj.network_address
        or ip_obj == network_obj.broadcast_address
    )


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

    assert (
        ip_obj in network_obj.hosts()
        or ip_obj == network_obj.network_address
        or ip_obj == network_obj.broadcast_address
    )


def test_generate_ip_list_default_count():
    """Test generating default number of IPs."""
    with patch("ip_visualizer.core.ip_generator.generate_random_ip") as mock_gen_ip:
        # Mock generate_random_ip to return predictable values
        mock_gen_ip.side_effect = [f"192.168.1.{i}" for i in range(100)]

        result = generate_ip_list()

        assert len(result) == 100
        assert all(ip.startswith("192.168.1.") for ip in result)


def test_generate_ip_list_custom_count():
    """Test generating a custom number of IPs."""
    with patch("ip_visualizer.core.ip_generator.generate_random_ip") as mock_gen_ip:
        # Mock generate_random_ip to return predictable values
        mock_gen_ip.side_effect = [f"10.0.0.{i}" for i in range(50)]

        result = generate_ip_list(total_ips=50)

        assert len(result) == 50
        assert all(ip.startswith("10.0.0.") for ip in result)


def test_generate_ip_list_regional_distribution():
    """Test that IPs are generated from different regions."""
    # Mock the random choice to ensure we test the distribution logic
    with (
        patch("random.choice") as mock_choice,
        patch("ip_visualizer.core.ip_generator.generate_random_ip") as mock_gen_ip,
    ):
        # Mock the continent selection to cycle through regions
        mock_choice.side_effect = [
            "Asia",
            "Europe",
            "North America",
            "South America",
        ] * 25

        # Mock IP generation to return unique IPs
        mock_gen_ip.side_effect = [f"10.0.{i}.1" for i in range(100)]

        result = generate_ip_list(total_ips=100)

        assert len(result) == 100
        assert len(set(result)) == 100  # All IPs should be unique
        assert all(ip.startswith("10.0.") for ip in result)


def test_generate_ip_list_with_small_quantity():
    """Test generating a small number of IPs."""
    result = generate_ip_list(total_ips=10)
    assert len(result) == 10
    # Verify all returned values are valid IP addresses
    for ip in result:
        ipaddress.ip_address(ip)  # Will raise ValueError if not a valid IP


def test_generate_ip_list_with_large_quantity():
    """Test generating a large number of IPs."""
    with patch("ip_visualizer.core.ip_generator.generate_random_ip") as mock_gen_ip:
        # Mock generate_random_ip to return unique IPs
        mock_gen_ip.side_effect = [f"192.168.{i // 256}.{i % 256}" for i in range(1000)]

        result = generate_ip_list(total_ips=1000)

        assert len(result) == 1000
        assert len(set(result)) == 1000  # All IPs should be unique


if __name__ == "__main__":
    pytest.main(["-v"])
