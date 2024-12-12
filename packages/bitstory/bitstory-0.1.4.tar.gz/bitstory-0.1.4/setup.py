# setup.py
from setuptools import setup, find_packages
from bitstory import __version__ 

setup(
    name="bitstory",
    version=__version__,
    description="A package for programmatic access to bitstory API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Gunnar Pope",
    author_email="gunnar@bitstory.ai",
    url="https://github.com/bitstory-ai/bitstory-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
		license="MIT",
    python_requires=">=3.10",
)
