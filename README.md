# IP Address Visualization

This project visualizes IP addresses from a CSV file on an interactive geographical map, showing the distribution and concentration of IP addresses across different regions.

## Prerequisites

- Python 3.7 or higher
- MaxMind GeoLite2 City database

## Setup

1. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Download the MaxMind GeoLite2 City database:
   - Go to https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
   - Sign up for a free account
   - Download the GeoLite2 City database (GeoLite2-City.mmdb)
   - Place the downloaded file in the project root directory

## Usage

1. Ensure your CSV file is in the project directory
2. Run the visualization script:
   ```bash
   python ip_visualizer.py
   ```
3. Open the generated `ip_heatmap.html` file in a web browser to view the interactive map

## Output

The script will generate an interactive HTML map (`ip_heatmap.html`) that shows:

- A heatmap visualization of IP address distribution
- Higher concentrations of IPs are shown in warmer colors
- You can zoom and pan the map to explore different regions

## Notes

- The visualization uses a heatmap to show IP address density
- Areas with more IP addresses will appear in warmer colors
- The map is interactive and can be zoomed and panned
