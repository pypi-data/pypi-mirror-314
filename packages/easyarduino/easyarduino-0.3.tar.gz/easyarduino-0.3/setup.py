
from setuptools import setup, find_packages

setup(
    name="easyarduino",
    version="0.3",
    description="A simple and easy-to-use Arduino control library using PyFirmata",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="AKM Korishee Apurbo",
    author_email="bandinvisible8@gmail.com",
    url="https://github.com/IMApurbo/easyarduino",
    packages=find_packages(),
    install_requires=[
        "pyfirmata",
        "pyserial",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
