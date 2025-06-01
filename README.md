# IP Address Visualization

This project visualizes IP addresses from a CSV file on an interactive geographical map, showing the distribution and concentration of IP addresses across different regions. It also includes utilities for generating random IP addresses for testing purposes.

## Prerequisites

- Python 3.12 or higher
- MaxMind GeoLite2 City database (for IP geolocation)

## Setup

1. Install the required Python packages:
   ```bash
   uv sync

   # Or pip ≥ 23.1
   pip install .
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

## Testing

Run the test suite with coverage report:

```bash
pytest --cov=./ --cov-report=term-missing --cov-report=html
```

This will:
- Run all tests
- Show test coverage in the terminal
- Generate an HTML coverage report in the `htmlcov` directory

Open `htmlcov/index.html` in a browser to view the detailed coverage report.

## Notes

- The visualization uses a heatmap to show IP address density
- Areas with more IP addresses will appear in warmer colors
- The map is interactive and can be zoomed and panned

## Code Quality

This project maintains a minimum test coverage of 80%. The test coverage report is generated automatically when running tests and can be viewed in the `htmlcov` directory.
