import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="open-gxipy",
    version="2.0.2403.9191",
    author="HS Soft",
    description="Python API to use with the HS Soft cameras.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/otabek-olimjonov/open_gxipy",
    packages=["gxipy"],
    install_requires=[
        "numpy",
        "Pillow"
        ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
