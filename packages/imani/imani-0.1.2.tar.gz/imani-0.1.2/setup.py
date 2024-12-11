# setup.py

from setuptools import setup, find_packages

setup(
    name="imani",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "MDAnalysis",
        "matplotlib",
        "joblib"
    ],
    entry_points={
        "console_scripts": [
            "imani_hydration=imani.run_hydration:main",
        ]
    },
    author="Melissa Jade Mitchell",
    description="Advanced molecular analysis tools for molecular dynamics simulations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/melissajadem/imani",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
