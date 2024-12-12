from setuptools import setup, find_packages

with open("README.md", 'r', encoding="utf-8") as fh:
	long_description = fh.read()

setup(
	name="em1l10",
	version="0.1.0",
	packages=find_packages(),
	install_requires=[],
	author="Emilio Arteaga",
	description="First Package",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://google.es",
)
