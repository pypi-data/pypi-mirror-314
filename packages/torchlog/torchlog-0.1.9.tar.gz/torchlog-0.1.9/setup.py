from setuptools import setup, find_packages

setup(
    name="torchlog",
    version="0.1.9",
    long_description=open("README.md").read(),
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7"
)
