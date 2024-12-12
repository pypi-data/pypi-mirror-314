from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='byzfl', # name of packe which will be package dir below project
    version='0.0.3',
    url='https://github.com/LPD-EPFL/byzfl',
    author='Geovani Rizk',
    author_email='geovani.rizk@epfl.ch',
    description='ByzFL Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["torch>=2.2.0", 
                      "torchvision>=0.17.0",
                      "numpy>=1.26.4",
                      "matplotlib>=3.8.3",
                      "scipy>=1.12.0"]
)
