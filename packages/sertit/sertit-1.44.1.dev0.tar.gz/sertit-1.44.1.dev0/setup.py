import setuptools

from sertit import (
    __author__,
    __author_email__,
    __description__,
    __documentation__,
    __title__,
    __url__,
    __version__,
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "tqdm",
        "lxml",
        "dill",
        "psutil",
        "geopandas>=0.14.4",
        "cloudpathlib[all]>=0.12.1",
        "xarray>=2024.06.0",
    ],
    extras_require={
        "colorlog": ["colorlog"],
        "full": [
            "rasterio>=1.3.10",
            "rioxarray>=0.10.0",
            "colorlog",
            "dask[complete]>=2024.5.1",
            "odc-geo>=0.4.6",
            "xarray-spatial>=0.3.6",
        ],
        "rasters_rio": ["rasterio>=1.3.10"],
        "rasters": ["rasterio>=1.3.10", "rioxarray>=0.10.0"],
        "dask": [
            "rasterio[s3]>=1.3.10",
            "rioxarray>=0.10.0",
            "dask[complete]>=2024.5.1",
            "odc-geo>=0.4.6",
            "xarray-spatial>=0.3.6",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_data={"": ["LICENSE", "NOTICE"]},
    include_package_data=True,
    python_requires=">=3.9",
    project_urls={
        "Bug Tracker": f"{__url__}/issues/",
        "Documentation": __documentation__,
        "Source Code": __url__,
    },
)
