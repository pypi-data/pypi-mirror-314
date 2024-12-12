from setuptools import setup, find_packages

setup(
    name="TkinterExtras",
    version="0.1.18",
    packages=find_packages(),
    install_requires=[],
    author="Marcus Collins",
    author_email="mjdj27123@gmail.com",
    description="Some extra classes and functions for tkinter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)