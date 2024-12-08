# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="randomcontent",  # The name of your package
    version="0.1.3",  # The version of your package
    author="Praful B Shankar",  # Your name or your organization's name
    description="A library for generating random text, numbers, and structured data.",  # A short description of your package
    packages=find_packages(),  # This automatically finds and includes all the packages in your project
    install_requires=[],  # List any dependencies your package has (e.g., numpy, pandas)
    include_package_data=True,
    author_email="prafulvishwakarmaq@gmail.com",    
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prafulacharya/randomcontent",  # Update with your repository URL    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Update if using a different license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10"
)

