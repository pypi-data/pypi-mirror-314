# setup.py

from setuptools import setup, find_packages

setup(
    name="randomcontent",  # The name of your package
    version="0.1.0",  # The version of your package
    author="Praful B Shankar",  # Your name or your organization's name
    description="A library for generating random text, numbers, and structured data.",  # A short description of your package
    packages=find_packages(),  # This automatically finds and includes all the packages in your project
    install_requires=[],  # List any dependencies your package has (e.g., numpy, pandas)
)

