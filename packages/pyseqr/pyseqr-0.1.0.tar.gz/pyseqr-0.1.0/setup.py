from setuptools import setup, find_packages

setup(
    name="pyseqr",
    version="0.1.0",
    packages=find_packages(),
    description="A Python library for sequence search and analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="John Curry",
    url="https://github.com/rattling/pyseqr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
