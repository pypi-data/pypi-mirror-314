from setuptools import setup

with open('/home/hassan/Documents/codes/deusfinance/multicallable/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    install_requires=required
)
