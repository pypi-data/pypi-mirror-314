import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thejsonlogger",
    version="0.0.3",
    author="Aaron Rueth",
    author_email="arueth@gmail.com",
    description="The JSON Logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rueth-io/thejsonlogger",
    project_urls={"Bug Tracker": "https://github.com/rueth-io/my-json-logger/issues"},
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Logging",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
