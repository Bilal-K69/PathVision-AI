"""Setup configuration for PathVision AI."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pathvision-ai",
    version="1.0.0",
    author="Bilal-K69",
    description="Interactive Pathfinding Visualization and Intelligent Analysis System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bilal-K69/PathVision-AI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pathvision=pathvision.main:main",
        ],
    },
)
