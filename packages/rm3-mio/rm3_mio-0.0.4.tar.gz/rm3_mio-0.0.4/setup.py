import setuptools

with open("README.md", "r", encoding = "utf-8") as f:
    long_description = f.read()

setuptools.setup(
    # Titles
    name = "rm3-mio",
    version = "0.0.4",
    author = "Shahrose Kasim",
    author_email = "rosemaster3000@gmail.com",
    url = "https://gitlab.com/RoseMaster3000/mio",
    
    # Description
    description = "Personal Python Utilites",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    
    # Configs
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(),
    install_requires = [],
    python_requires = ">=3.8"
)