from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytopomojo",
    version="0.1.1",
    description="A TopoMojo API Client",
    url="https://github.com/jbooz1/pytopomojo",
    packages=find_packages(),
    install_requires=["requests"],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
