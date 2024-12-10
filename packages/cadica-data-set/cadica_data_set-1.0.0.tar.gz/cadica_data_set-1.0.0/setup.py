from setuptools import setup, find_packages 

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="cadica_data_set",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.6",
) 