from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="live-gpio",
    version="3.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
        "pigpio",
        "Flask-SocketIO"
    ],
    entry_points={
        "console_scripts": [
            "live-gpio=live_gpio.app:main"
        ]
    },
    package_data={
        "live_gpio": ["templates/*.html", "static/*"]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)