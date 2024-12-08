from setuptools import setup, find_packages

setup(
    name="unique-picker",  # Package name (lowercase, hyphenated)
    version="0.0.1",       # Initial version
    author="Siraj Dal",
    author_email="write2siraj@gmail.com",
    description="A package for unique random selection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/unique-picker",  # GitHub repo URL
    packages=find_packages(),  # Automatically find subpackages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
