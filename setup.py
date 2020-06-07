import os

from setuptools import setup, find_packages

try:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "requirements.txt")) as f:
        required = [
            l.strip("\n") for l in f if l.strip("\n") and not l.startswith("#")
        ]
except IOError:
    required = []
    README = ""

setup(
    name="fantastic-api",
    packages=find_packages(),
    version="0.0.1",
    license="GPLv3+",
    description="fantastic-api is a test project",
    long_description_content_type="text/markdown",
    author="Amine Ben Asker",
    author_email="amine@eyacom.com",
    url="https://github.com/eyacom/fanstastic-api",
    install_requires=required,
    classifiers=[
        "Development Status :: 1 - Development",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
