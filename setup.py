from setuptools import setup, find_packages

setup(
    name="mancala_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pytest>=7.0.0",
        "pytest-cov>=3.0.0",
    ],
    python_requires=">=3.9",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Mancala game implementation with AI using Minimax algorithm",
    long_description=open("mancala_ai/README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 