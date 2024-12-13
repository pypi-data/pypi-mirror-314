from setuptools import setup, find_packages

VERSION = '0.0.12'
DESCRIPTION = 'A simple module to assist in physics bachelor'

# Setting up
setup(
    name="physictools",
    version=VERSION,
    author="Paul Welte",
    description=DESCRIPTION,
    packages=["physictools"],
    install_requires=['scipy','numpy']
)