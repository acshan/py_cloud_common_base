import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloud_common_lib",
    version="0.0.1",
    author="Sage",
    author_email="sage.ace@outlook.com",
    description="cloud common lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acshan/py_cloud_common_base",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
