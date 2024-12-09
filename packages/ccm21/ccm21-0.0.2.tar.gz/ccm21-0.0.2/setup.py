from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ccm21",
    version="0.0.2",
    author="Henrique Silveira",
    author_email="henrique@minimundo.com.br",
    description="A package to control Midea CCM21 data converter modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oosilveir4/ccm21.py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'httpx>=0.24.1',
        'xmltodict>=0.13.0',
        'aiohttp>=3.8.5'
    ]
)
