from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import os

extensions = [
    Extension("my_module", ["src/my_module.pyx"])
]

setup(
    name="openimagepdemo",
    version="0.1.0",
    description="A sample Python module compiled with Cython",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    ext_modules=cythonize(extensions),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
