from setuptools import setup, find_packages

setup(
    name="betrand-ngoh-mutagha-version",  # Use hyphens
    version="0.2.11",  # Ensure this is the correct and latest version
    author="BETRAND MUTAGHA",
    author_email="mutagha2@gmail.com",
    url="https://github.com/Betrand1999/cicd",
    packages=find_packages(),
    include_package_data=True,  # Ensure package data is included
    install_requires=[
        "flask",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
