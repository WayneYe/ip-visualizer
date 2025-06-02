from setuptools import find_packages, setup

setup(
    name="ip-visualizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.2.6",
        "pandas>=2.2.3",
        "folium>=0.19.5",
        "geoip2>=5.1.0",
        "typer>=0.9.0",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "ip-visualizer=ip_visualizer.cli:app",
        ],
    },
    python_requires=">=3.12",
)
