from setuptools import setup, find_packages

# Dynamically read the version from the package
def get_version():
    version_file = "src/anaug/version.py"
    with open(version_file) as f:
        for line in f:
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Version not found.")

setup(
    name="anaug",
    version=get_version(),  # Use the dynamically read version
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
