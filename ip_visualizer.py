# /// script
# requires-python = ">=3.13"
# dependencies = [
# "numpy==2.2.6",
# "pandas==2.2.3",
# "folium==0.19.5",
# "geoip2==5.1.0",
# ]
# ///
import pandas as pd
import folium
from folium.plugins import HeatMap
import geoip2.database
from collections import defaultdict


def load_ip_data(csv_file):
    """Load IP addresses from CSV file."""
    print("Loading data from CSV...")
    df = pd.read_csv(csv_file)
    return df["_source.cg\.detail\.remote_addr"].dropna().unique()


def get_ip_locations(ip_addresses):
    """Convert IP addresses to geographical coordinates using MaxMind GeoLite2 database."""
    print("Converting IPs to locations...")
    locations = []
    ip_counts = defaultdict(int)

    # You'll need to download the GeoLite2 database from MaxMind
    # https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
    try:
        with geoip2.database.Reader("GeoLite2-City.mmdb") as reader:
            for ip in ip_addresses:
                try:
                    response = reader.city(ip)
                    lat = response.location.latitude
                    lon = response.location.longitude
                    if lat and lon:
                        locations.append([lat, lon])
                        ip_counts[(lat, lon)] += 1
                except Exception as e:
                    print(f"Error looking up IP {ip}: {str(e)}")
                    continue
    except FileNotFoundError:
        print("Error: GeoLite2-City.mmdb not found. Please download it from MaxMind.")
        return None, None

    return locations, ip_counts


def create_heatmap(locations, ip_counts):
    """Create an interactive heatmap using Folium."""
    print("Creating heatmap...")
    # Create a map centered at a default location
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add heatmap layer
    heat_data = [[lat, lon, count] for (lat, lon), count in ip_counts.items()]
    HeatMap(heat_data).add_to(m)

    # Save the map
    m.save("ip_heatmap.html")
    print("Map saved as ip_heatmap.html")


def main():
    csv_file = "path_to_my_csv_file.csv"

    # Load IP addresses
    ip_addresses = load_ip_data(csv_file)
    # Remove ":[port]" from the IP addresses
    ip_addresses = [ip.split(":")[0] for ip in ip_addresses]
    print(f"Found {len(ip_addresses)} unique IP addresses")

    # Convert IPs to locations
    locations, ip_counts = get_ip_locations(ip_addresses)
    if locations:
        print(f"Successfully geolocated {len(locations)} IP addresses")

        # Create and save the heatmap
        create_heatmap(locations, ip_counts)
    else:
        print("Failed to create visualization due to missing GeoLite2 database")


if __name__ == "__main__":
    main()
