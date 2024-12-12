import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crawldo",
    version="0.0.4",
    author="twj",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "crawldo"},
    packages=setuptools.find_packages(where="crawldo"),
    python_requires=">=3.6",
)
