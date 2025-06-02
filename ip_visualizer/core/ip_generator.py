import ipaddress
import random
import sys


def generate_random_ip(network_prefix: str):
    """Generates a random IP address within a given network prefix."""
    network = ipaddress.ip_network(network_prefix, strict=False)
    # Get the integer representation of the network address
    network_int = int(network.network_address)
    # Get the integer representation of the broadcast address
    broadcast_int = int(network.broadcast_address)

    # Generate a random integer within the valid host range (excluding network and broadcast addresses)
    # If the network only has 1 or 2 possible addresses (like /31 or /32), handle it
    if network.num_addresses <= 2:  # noqa: PLR2004
        random_ip_int = network_int
    else:
        random_ip_int = random.randint(network_int + 1, broadcast_int - 1)  # noqa: S311

    return str(ipaddress.ip_address(random_ip_int))


def generate_ip_list(total_ips: int = 100) -> list[str]:
    """
    Generates a list of IP addresses with a specified regional distribution.
    """
    ip_addresses: list[str] = []

    # Define approximate IP ranges for each continent.
    # These are illustrative and not exhaustive or strictly geolocated.
    ip_ranges = {
        "Asia": [
            "1.0.0.0/8",
            "27.0.0.0/8",
            "36.0.0.0/8",
            "42.0.0.0/8",
            "49.0.0.0/8",
            "58.0.0.0/8",
            "59.0.0.0/8",
            "60.0.0.0/8",
            "61.0.0.0/8",
            "101.0.0.0/8",
            "103.0.0.0/8",
            "112.0.0.0/8",
            "113.0.0.0/8",
            "114.0.0.0/8",
            "115.0.0.0/8",
            "116.0.0.0/8",
            "117.0.0.0/8",
            "118.0.0.0/8",
            "119.0.0.0/8",
            "120.0.0.0/8",
            "121.0.0.0/8",
            "122.0.0.0/8",
            "123.0.0.0/8",
            "124.0.0.0/8",
            "125.0.0.0/8",
            "126.0.0.0/8",
            "140.0.0.0/8",
            "150.0.0.0/8",
            "153.0.0.0/8",
            "175.0.0.0/8",
            "180.0.0.0/8",
            "182.0.0.0/8",
            "183.0.0.0/8",
            "202.0.0.0/8",
            "203.0.0.0/8",
            "210.0.0.0/8",
            "211.0.0.0/8",
            "218.0.0.0/8",
            "219.0.0.0/8",
            "220.0.0.0/8",
            "221.0.0.0/8",
            "222.0.0.0/8",
            "223.0.0.0/8",
        ],
        "Europe": [
            "2.0.0.0/8",
            "5.0.0.0/8",
            "31.0.0.0/8",
            "37.0.0.0/8",
            "46.0.0.0/8",
            "62.0.0.0/8",
            "66.0.0.0/8",
            "77.0.0.0/8",
            "78.0.0.0/8",
            "79.0.0.0/8",
            "80.0.0.0/8",
            "81.0.0.0/8",
            "82.0.0.0/8",
            "83.0.0.0/8",
            "84.0.0.0/8",
            "85.0.0.0/8",
            "86.0.0.0/8",
            "87.0.0.0/8",
            "88.0.0.0/8",
            "89.0.0.0/8",
            "90.0.0.0/8",
            "91.0.0.0/8",
            "92.0.0.0/8",
            "93.0.0.0/8",
            "94.0.0.0/8",
            "95.0.0.0/8",
            "109.0.0.0/8",
            "141.0.0.0/8",
            "146.0.0.0/8",
            "151.0.0.0/8",
            "176.0.0.0/8",
            "178.0.0.0/8",
            "185.0.0.0/8",
            "188.0.0.0/8",
            "193.0.0.0/8",
            "194.0.0.0/8",
            "212.0.0.0/8",
            "213.0.0.0/8",
            "217.0.0.0/8",
        ],
        "North America": [
            "3.0.0.0/8",
            "4.0.0.0/8",
            "7.0.0.0/8",
            "8.0.0.0/8",
            "12.0.0.0/8",
            "18.0.0.0/8",
            "23.0.0.0/8",
            "24.0.0.0/8",
            "50.0.0.0/8",
            "63.0.0.0/8",
            "64.0.0.0/8",
            "65.0.0.0/8",
            "67.0.0.0/8",
            "68.0.0.0/8",
            "69.0.0.0/8",
            "70.0.0.0/8",
            "71.0.0.0/8",
            "72.0.0.0/8",
            "73.0.0.0/8",
            "74.0.0.0/8",
            "75.0.0.0/8",
            "76.0.0.0/8",
            "96.0.0.0/8",
            "97.0.0.0/8",
            "98.0.0.0/8",
            "99.0.0.0/8",
            "100.0.0.0/8",
            "104.0.0.0/8",
            "107.0.0.0/8",
            "108.0.0.0/8",
            "142.0.0.0/8",
            "143.0.0.0/8",
            "144.0.0.0/8",
            "147.0.0.0/8",
            "155.0.0.0/8",
            "156.0.0.0/8",
            "157.0.0.0/8",
            "158.0.0.0/8",
            "159.0.0.0/8",
            "160.0.0.0/8",
            "161.0.0.0/8",
            "162.0.0.0/8",
            "164.0.0.0/8",
            "165.0.0.0/8",
            "166.0.0.0/8",
            "167.0.0.0/8",
            "168.0.0.0/8",
            "169.0.0.0/8",
            "170.0.0.0/8",
            "172.0.0.0/8",
            "173.0.0.0/8",
            "174.0.0.0/8",
            "192.0.0.0/8",
            "198.0.0.0/8",
            "204.0.0.0/8",
            "205.0.0.0/8",
            "206.0.0.0/8",
            "207.0.0.0/8",
            "208.0.0.0/8",
            "209.0.0.0/8",
        ],
        "South America": [
            "38.0.0.0/8",
            "45.0.0.0/8",
            "131.0.0.0/8",
            "138.0.0.0/8",
            "139.0.0.0/8",
            "167.0.0.0/8",
            "177.0.0.0/8",
            "179.0.0.0/8",
            "181.0.0.0/8",
            "186.0.0.0/8",
            "187.0.0.0/8",
            "189.0.0.0/8",
            "190.0.0.0/8",
            "200.0.0.0/8",
            "201.0.0.0/8",
        ],
    }

    distribution = {
        "Asia": int(total_ips * 0.30),
        "Europe": int(total_ips * 0.30),
        "North America": int(total_ips * 0.30),
        "South America": int(total_ips * 0.10),
    }

    # Generate IPs for each region
    for region, count in distribution.items():
        if not ip_ranges[region]:
            print(f"Warning: No IP ranges defined for {region}. Skipping.")
            continue

        for _ in range(count):
            selected_range = random.choice(ip_ranges[region])  # noqa: S311
            try:
                ip_addresses.append(generate_random_ip(selected_range))
            except ValueError as e:
                print(f"Error generating IP for {region} from {selected_range}: {e}")
                # Fallback or retry could be implemented here

    # Shuffle the list to mix the regions
    random.shuffle(ip_addresses)

    return ip_addresses


def main(count: int = 100):
    # Generate the list of 100 IP addresses
    ip_list = generate_ip_list(total_ips=count)

    # Print the generated IP addresses
    for i, ip in enumerate(ip_list):
        print(f"{i + 1}-> {ip}")

    print(f"\nGenerated {len(ip_list)} IP addresses.")


if __name__ == "__main__":
    count = int(sys.argv[1])
    main(count)
