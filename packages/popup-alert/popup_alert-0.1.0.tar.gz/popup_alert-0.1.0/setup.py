from setuptools import setup, find_packages

setup(
    name="popup-alert",
    version="0.1.0",
    description="A simple module to show Windows message box alerts.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="JadXV",
    author_email="dreamedofit@gmail.com",
    url="https://github.com/JadXV/popup",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8", 
)
