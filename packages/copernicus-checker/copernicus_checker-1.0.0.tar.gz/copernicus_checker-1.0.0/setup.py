from setuptools import setup, find_packages

setup(
    name="copernicus_checker",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pymongo",
        "copernicusmarine",
    ],
    entry_points={
        "console_scripts": [
            "copernicus_checker=app:main",  # Makes `copernicus_checker` runnable
        ],
    },
    description="Copernicus Marine API with MongoDB duplication checking.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/copernicus_checker",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
