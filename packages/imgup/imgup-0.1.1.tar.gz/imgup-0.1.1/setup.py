from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="imgup",
    version="0.1.1",
    description="A CLI tool to upload image to imgbb.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="decryptable",
    author_email="hello@decryptable.dev",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "imgup=imgup.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
