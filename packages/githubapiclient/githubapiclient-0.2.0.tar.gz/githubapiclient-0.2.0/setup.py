from setuptools import setup, find_packages

setup(
    name="githubapiclient",
    version="0.2.0",
    author="Peter Nyando",
    author_email="anomalous254@gmail.com",
    description="A Python library to interact with the GitHub API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anomalous254/githubapiclient", 
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
