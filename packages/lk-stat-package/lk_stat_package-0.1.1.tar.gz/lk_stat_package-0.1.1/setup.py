from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Define the extension
extensions = [
    Extension(
        "lk_stat_package.lk_stat",
        ["lk_stat_package/lk_stat.pyx"],
        include_dirs=[np.get_include()],
    )
]

# Setup script
setup(
    name="lk_stat_package",
    version="0.1.1",
    description="A Cython-based package for computing the Laffler-Kinman statistic.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Princy Ranaivomanana",
    author_email="rtprincy@gmail.com",
    packages=["lk_stat_package"],
    ext_modules=cythonize(extensions),
    zip_safe=False,
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
    ],
)

