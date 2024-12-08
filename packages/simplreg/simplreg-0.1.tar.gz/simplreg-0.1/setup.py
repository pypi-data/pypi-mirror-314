from setuptools import setup, find_packages

setup(
    name="simplreg",
    version="0.1",
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