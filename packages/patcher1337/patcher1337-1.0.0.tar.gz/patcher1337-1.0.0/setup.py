from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="patcher1337",
    version="1.0.0",
    author="moshouhot",
    author_email="moshouhot@gmail.com",
    description="A Python library for handling 1337 format patch files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moshouhot/patcher1337",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
