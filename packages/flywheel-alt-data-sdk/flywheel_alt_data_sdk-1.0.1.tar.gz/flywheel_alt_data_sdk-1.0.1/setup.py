from setuptools import setup, find_packages

setup(
    name="flywheel_alt_data_sdk",
    version="1.0.1",
    description="A Python wrapper for the Flywheel Digital Alt Data API",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires=">=3.7",
)
