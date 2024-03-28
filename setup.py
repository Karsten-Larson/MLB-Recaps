from setuptools import find_packages, setup

with open("README.md", "r") as f:
	long_description = f.read()

setup(
    name="mlbrecaps",
    version="0.0.7",
    description="Package that gathers information on given MLB games",
    packages=find_packages(include=["mlbrecaps"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrRedwing/MLB-Recaps",
    author="Karsten Larson",
    author_email="karsten.larson.1@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy>=1.13.0',
                      'pandas >= 1.0.3',
                      'beautifulsoup4>=4.4.0',
                      'requests>=2.18.1',
                      'lxml>=4.2.1',],
    extras_require={
        "dev": ["twine"]
    },
    python_requires=">=3.10",
    include_package_data=True,
    package_data={'': ['data/*.csv']},
)
