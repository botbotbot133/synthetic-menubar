#!/usr/bin/env python3
"""Setup script for synthetic-menubar"""

from setuptools import setup

setup(
    name="synthetic-menubar",
    version="1.0.1",
    description="Menu bar app for monitoring Synthetic API credits",
    py_modules=["synthetic_menubar_app"],
    python_requires=">=3.8",
    install_requires=[
        "rumps>=0.4.0",
    ],
    entry_points={
        "console_scripts": [
            "synthetic-menubar=synthetic_menubar_app:main",
        ],
    },
)
