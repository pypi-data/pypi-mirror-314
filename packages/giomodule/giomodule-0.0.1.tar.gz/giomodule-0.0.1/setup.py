import setuptools
from pathlib import Path

# python3 setup.py sdist bdist_wheel

setuptools.setup(
    name="giomodule",
    version="0.0.1",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(
        exclude=["mocks", "test"]
    )
)

