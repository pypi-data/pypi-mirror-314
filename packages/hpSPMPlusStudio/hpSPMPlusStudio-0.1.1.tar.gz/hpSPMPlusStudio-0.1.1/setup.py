from setuptools import setup, find_packages

setup(
    name="hpSPMPlusStudio",
    version="0.1.1",
    author="NanoMagnetics Instruments",
    author_email="nmi.swteam@nano.com.tr",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)