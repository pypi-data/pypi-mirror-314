from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="simplreg",
    version="0.2",
    author="Mridul",
    author_email="jain.mridul.20@gmail.com",
    description="A simple machine learning package for forecasting and classification",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Spinachboul/simplreg",
    packages=find_packages(),
    install_requires = [
        "pandas",
        "numpy",
        "scikit-learn",
        "tabulate",
        "matplotlib",
        "seaborn"
    ],
    pytest_requires=">=3.6",
)