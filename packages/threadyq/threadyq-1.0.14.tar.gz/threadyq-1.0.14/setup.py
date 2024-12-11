from setuptools import setup, find_packages
import codecs
import os

# Get the absolute path to the directory containing this file
here = os.path.abspath(os.path.dirname(__file__))

# Read the long description from the README file
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

# Define the version of the package
VERSION = '1.0.14'

# Short description of the package
DESCRIPTION = '''ThreadyQ is a Python library designed to simplify and extend the capabilities of threading and queue management. This package provides an abstraction layer over Python's built-in threading and queue modules, enabling developers to create, manage, and synchronize tasks efficiently in multi-threaded applications.'''

# Setting up the package
setup(
    name="threadyq",
    version=VERSION,
    author="Muhammed Rahil M",
    author_email="muhammedrahilmadathingal@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    url="https://github.com/muhammedrahil/ThreadyQ",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'threading', 'queue'],
    # license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",  # Add license if applicable
    ]
)
