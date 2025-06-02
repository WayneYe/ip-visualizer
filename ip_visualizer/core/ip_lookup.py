#!/usr/bin/env python3
import json
import sys

import geoip2.database


def lookup_ip(ip: str) -> dict[str, str | float | None]:
    """Look up an IP address in the GeoLite2 database."""
    try:
        with geoip2.database.Reader("./data/GeoLite2-City.mmdb") as reader:
            response = reader.city(ip)
            return {
                "ip": ip,
                "city": response.city.name,
                "country": response.country.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "timezone": response.location.time_zone,
                "postal_code": response.postal.code,
                "continent": response.continent.name,
            }
    except Exception as e:
        print(f"Error looking up IP {ip}: {e!s}")
        return {}


REQUIRED_ARG_COUNT = 2
def main():
    if len(sys.argv) != REQUIRED_ARG_COUNT:
        print("Usage: python ip_lookup.py <ip_address>")
        print("Example: python ip_lookup.py 8.8.8.8")
        sys.exit(1)

    ip = sys.argv[1]
    result = lookup_ip(ip)

    if result:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
