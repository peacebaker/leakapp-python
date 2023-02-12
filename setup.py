#!/usr/bin/env python
from pathlib import Path
from distutils.core import setup

# The text of the README file
parent_path = Path(__file__).parent
readme_path = Path(f"{parent_path}/README.md")
README = readme_path.read_text()

setup(
    name='leakapp',
    version='0.1.0',
    description="Lea Kapp's personal utilities.",
    long_description=README,
    long_description_content_type="text/markdown",
    author='Lea Kapp',
    url='https://www.python.org/sigs/distutils-sig/',
    packages=['leakapp.utils', 'leakapp.dicebag'],
    install_requires=[],
)