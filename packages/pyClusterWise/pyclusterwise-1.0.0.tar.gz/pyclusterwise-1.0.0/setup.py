from setuptools import setup, find_packages

setup(
    name="pyClusterWise",  # Name of your package
    version="1.0.0",  # Initial version
    description="A Python package for dynamic clustering analysis with multiple methods and uncertainty evaluation.",
    long_description=open("README.md").read(),  # Include detailed description
    long_description_content_type="text/markdown",  # Markdown formatting
    author="Behnam Sadeghi",  # Replace with your name
    author_email="z5218858@zmail.unsw.edu.au",  # Replace with your email
    license="MIT",
    packages=find_packages(),  # Automatically find all packages
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "scikit-learn",
        "scipy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
