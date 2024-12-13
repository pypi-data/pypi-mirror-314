from setuptools import setup, find_packages

# Reading the content of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="copernicus_checker",  # Updated project name
    version="1.0.2",  # Update the version as needed
    description="A Python package for checking duplicate dataset requests in Copernicus projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # If your README is Markdown
    packages=find_packages(),  # Automatically find and include your packages
    install_requires=[
        "pymongo",  # Add dependencies required for your project
    ],
    classifiers=[
        "Programming Language :: Python :: 3",  # Specify the supported programming language
        "License :: OSI Approved :: MIT License",  # Specify your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify the minimum Python version requirement
)
