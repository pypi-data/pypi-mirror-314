from setuptools import setup, find_packages

setup(
    name="supertab",
    version="1.0.1",
    description="Reusable library for tab management using SQLAlchemy",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ascendeum",
    author_email="engineering@ascendeum.com",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy>=1.3",
        "PyMySQL>=1.0",
    ],
    python_requires=">=3.6",
)
