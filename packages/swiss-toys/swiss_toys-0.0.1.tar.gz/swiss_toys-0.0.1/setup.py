from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="swiss_toys",
    version="0.0.1",
    author="azai",
    author_email="fmyblack@gmail.com",
    description="一个实用的Python工具箱",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fmyblack/swiss_toys",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)