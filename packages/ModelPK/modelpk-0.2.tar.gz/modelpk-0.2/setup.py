from setuptools import setup, find_packages
setup(
    name = "ModelPK",
    version = "0.2",
    author="Jia Liang",
    author_email="jyliang@uw.edu",
    description="ModelPK is a package designed to extract basic information about the pharmacokinetic profile of a drug from experimental data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jyliang27/ModelPK",
    download_url="https://github.com/jyliang27/ModelPK/archive/refs/tags/v0.2.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages= find_packages()
)