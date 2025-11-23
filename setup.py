"""
SPDX-License-Identifier: MIT
Setup configuration for Emergent Code
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="emergent-code",
    version="0.4.0",
    author="Emergent Code Team",
    author_email="",
    description="Revolutionary code generation using LJPW Framework and fractal composition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/emergent-code",
    packages=find_packages(exclude=["tests", "experiments", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0.1,<7.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0,<8.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "black>=23.7.0,<24.0.0",
            "ruff>=0.0.285,<1.0.0",
            "mypy>=1.5.0,<2.0.0",
        ],
        "docs": [
            "sphinx>=7.1.0,<8.0.0",
            "sphinx-rtd-theme>=1.3.0,<2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "emergent-grow=master_grower:main",
            "emergent-test=run_all_tests:main",
            "emergent-validate=validate_fractal_proof:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
