from setuptools import setup, find_packages

setup(
    name="SWJFF",
    version="1.0.0.0",
    author="flamfrostboio",
    description="A module that serializes/deserializes data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/flamfrosticboio/SWJFF-Module-Python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "cryptography",
        "zstandard"
    ],
)
