from setuptools import setup, find_packages

setup(
    name="bctf",  # Name of your module
    version="0.1",  # Version of the module
    packages=find_packages(),
    install_requires=[],  # List of dependencies
    author="Yashwant Gokul P",
    author_email="your.email@example.com",
    description="""The FileHandler module provides simple and efficient functions for reading, writing, and appending data to various file formats including .txt, .dat, and .csv. It supports handling text, binary, and CSV data with automatic format detection based on file extension. This module is ideal for basic file operations, making it easy to work with different file types in Python without requiring complex file management.""",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust according to the license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)