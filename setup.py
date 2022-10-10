from setuptools import setup, find_packages

setup(
    name="dogdash",
    author="goyder",
    packages=find_packages("src"),
    package_dir={"": "src"}
)