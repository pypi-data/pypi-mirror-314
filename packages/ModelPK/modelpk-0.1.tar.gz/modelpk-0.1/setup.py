from setuptools import setup, find_packages
setup(
    name = "ModelPK",
    version = "0.1",
    author="Jia Liang",
    author_email="jyliang@uw.edu",
    description="ModelPK is a package designed to extract basic information about the pharmacokinetic profile of a drug from experimental data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jyliang27/ModelPK",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where='/ModelPK'),  # Specify the source directory
    package_dir={'': 'ModelPK'},
)