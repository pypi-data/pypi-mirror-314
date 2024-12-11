from setuptools import setup, find_packages

setup(
    name="MatchFinder",
    version="1.0.3",
    description="A Python package for finding similar strings with advanced formatting options.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Manoj Shetty K",
    author_email="shettykmanojmask@gmail.com",
    url="https://github.com/memanja/MatchFinder",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
