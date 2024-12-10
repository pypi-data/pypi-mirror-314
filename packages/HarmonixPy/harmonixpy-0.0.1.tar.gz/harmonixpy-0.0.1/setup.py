"""setup tools for package"""
from setuptools import setup, find_packages

setup(
    name="HarmonixPy",  # Package name (should be unique)
    version="0.0.1",  # Versioning
    packages=find_packages(),  # Automatically finds subpackages
    install_requires=[
        "flask",  # Add any core dependencies for your package
    ],
    include_package_data=True,  # Include non-Python files (e.g., HTML)
    description="A simple module for serving HTML and managing dependencies with Flask.",
    long_description=open("README.md", encoding="utf-8").read(),  # Use README for detailed info
    long_description_content_type="text/markdown",  # README format
    author="Taripretei Zidein",
    author_email="inspirante01@gmail.com",
    url="https://github.com/d-inspiration/HarmonixPy",  # URL to the project repo
    classifiers=[  # Optional: Categorize your project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Compatible Python version
)
