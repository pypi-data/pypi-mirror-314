from setuptools import find_packages, setup


setup(
    name="vincam",
    version="2.0.25",
    packages=find_packages(),
    install_requires=["numpy", "comtypes"],
    python_requires=">=3.11",
)