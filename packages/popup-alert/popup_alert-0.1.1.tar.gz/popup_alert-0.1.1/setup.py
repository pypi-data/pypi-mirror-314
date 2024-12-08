import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "popup-alert",
    version = "0.1.1",
    author = "JadXV",
    author_email = "dreamedofit@gmail.com",
    description = "A simple package to create popup alerts in Python",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/JadXV/popup",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.8"
)