import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpyg321",
    version="1.3.0",
    author="4br3mm0rd",
    author_email="4br3mm0rd@gmail.com",
    description="mpg321 wrapper for python - command line music player",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4br3mm0rd/mpyg321",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
