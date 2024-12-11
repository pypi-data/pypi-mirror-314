import pathlib
from setuptools import setup, find_packages

setup(
    name="tensorflow_helper_cnndnn",
    version="0.1.1",
    description="Helper package for TensorFlow CNN and DNN (dummy)",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/SA-Ahmed-W/tensorflow_helper_cnndnn",
    author="saaw",
    author_email="aasimahmedsiddiqui45666@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10,<3.13",
    install_requires=[
        "tensorflow",
        "scikit-learn",
        "matplotlib"
    ]
)
