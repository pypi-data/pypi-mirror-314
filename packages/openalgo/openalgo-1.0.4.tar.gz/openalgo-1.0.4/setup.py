from setuptools import setup, find_packages
import os

# Read the contents of README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Read version from __init__.py
with open(os.path.join(os.path.dirname(__file__), "openalgo", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="openalgo",
    version=version,
    description="Python library for algorithmic trading with OpenAlgo - Accounts, Orders, and Market Data APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="OpenAlgo",
    author_email="support@openalgo.in",
    url="https://docs.openalgo.in",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.2.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords=[
        "trading",
        "algorithmic-trading",
        "finance",
        "stock-market",
        "api-wrapper",
        "openalgo",
        "market-data",
        "trading-api",
        "stock-trading"
    ],
    project_urls={
        "Documentation": "https://docs.openalgo.in",
        "Source": "https://github.com/openalgo/openalgo-python",
        "Tracker": "https://github.com/openalgo/openalgo-python/issues",
    },
)
