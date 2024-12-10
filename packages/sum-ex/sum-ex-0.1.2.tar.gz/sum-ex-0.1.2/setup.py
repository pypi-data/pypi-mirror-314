#### **5. `setup.py`**
# This is the main configuration file:
from setuptools import setup, find_packages

setup(
    name="sum-ex",  # Package name
    version="0.1.2",  # Initial version
    author="Devanand",  # Replace with your name
    author_email="sanjaydeva1605@gmail.com",  # Replace with your email
    description="A simple Python package for math operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://vipstech.in",  # Optional: add a URL for documentation or GitHub
    packages=find_packages(),  # Automatically find all packages
    python_requires=">=3.6",
)
