from setuptools import setup, find_packages

setup(
    name="tmodelviz",
    version="1.1.0",
    author="Shajesh Sharma",
    author_email="shajesh.sharma@colorado.edu",
    description="A package for Tellurium model visualization.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tmodelviz",  # Replace with your GitHub repository URL
    packages=find_packages(),
    install_requires=[
        "tellurium>=2.1.6",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "ipywidgets>=7.6.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)