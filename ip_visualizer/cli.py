"""Command-line interface for IP Visualizer."""

import typer
from pprint import pprint

app = typer.Typer(help="IP Visualizer - Visualize IP addresses on a map.")


@app.command()
def generate_ips(count: int = 100):
    """Generate random IP addresses."""
    from ip_visualizer.core.ip_generator import main as ip_generator_main

    ip_generator_main(count)


@app.command()
def lookup_ip(ip: str):
    """Look up an IP address in the GeoLite2 database."""
    from ip_visualizer.core.ip_lookup import lookup_ip

    pprint(lookup_ip(ip))


@app.command()
def visualize():
    """Generate a heatmap of IP addresses."""
    from ip_visualizer.core.ip_visualizer import main as visualize_main

    visualize_main()


if __name__ == "__main__":
    app()
