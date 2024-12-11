from setuptools import setup, find_packages

setup(
    name="pytopomojo",
    version="0.1.0",
    description="A TopoMojo API Client",
    url="https://github.com/jbooz1/pytopomojo",
    packages=find_packages(),
    install_requires=["requests"],
)
