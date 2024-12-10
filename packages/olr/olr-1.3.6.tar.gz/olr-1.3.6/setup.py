import os
import setuptools
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name="olr",
    version="1.3.6",
    author="Mathew Fok",
    author_email="quiksilver67213@yahoo.com",
    description="olr: Optimal Linear Regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/MatHatter",
    packages=setuptools.find_packages(),
    install_requires=['pandas>=1.0.0', 'numpy>=1.18.0'],
    data_files= [('Lib\site-packages\olr', ['data\crudeoildata.csv'])],
    py_modules=['__init__', 'olr_function'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)


