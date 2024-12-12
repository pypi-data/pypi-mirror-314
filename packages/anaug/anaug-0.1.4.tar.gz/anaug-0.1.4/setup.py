from setuptools import setup, find_packages

__version__ = "0.1.4"

setup(
    name="anaug",
    version=__version__,
    description="AnAugment: A Python library for diverse data augmentation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="lunovian",
    author_email="nxan2911@gmail.com",
    url="https://github.com/lunovian/an-augment",
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
        "scipy>=1.5.0",
        "opencv-python>=4.5.0"
    ],
)