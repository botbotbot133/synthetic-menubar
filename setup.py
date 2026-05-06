#!/usr/bin/env python3
"""Setup script for synthetic-menubar"""

from setuptools import setup, find_packages

setup(
    name="synthetic-menubar",
    version="1.0.5",
    description="Menu bar app for monitoring Synthetic API credits",
    long_description="A macOS menu bar app that displays Synthetic API usage in real-time.",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "rumps>=0.4.0",
        "pyobjc-core>=10.0",
        "pyobjc-framework-Cocoa>=10.0",
    ],
    entry_points={
        "console_scripts": [
            "synthetic-menubar=synthetic_menubar:main",
        ],
    },
    url="https://github.com/botbotbot133/synthetic-menubar",
    author="botbotbot133",
    license="MIT",
    include_package_data=True,
)
