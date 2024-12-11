import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="dsl-dict-analyser",
    version="0.0.1",
    author="Feliks Peegel",
    author_email="felikspeegel@outlook.com",
    description="A Python package for analysing dsl dictionaries. Dsl dictionary is a dict type for lingvo app.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felikspeegel/dsl_dict_analyser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
