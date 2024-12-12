import gluepy
import setuptools


def read_requirements(filename):
    """Read requirements file and clean up lines."""
    with open(f"./requirements/{filename}") as f:
        return [
            line.strip()
            for line in f.read().split("\n")
            if line.strip() and not line.startswith("#") and not line.startswith("-r")
        ]


# Read all requirement files
requirements_base = read_requirements("base.txt")
requirements_dev = read_requirements("dev.txt")
requirements_digitalocean = read_requirements("digitalocean.txt")
requirements_gcp = read_requirements("gcp.txt")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gluepy",
    version=gluepy.VERSION,
    author="Marcus Lind",
    author_email="marcuslind90@gmail.com",
    description="A framework for data scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gluepy/gluepy",
    packages=setuptools.find_packages(),
    scripts=["gluepy/bin/gluepy-cli.py"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.9",
    install_requires=requirements_base,
    extras_require={
        "all": requirements_base
        + requirements_dev
        + requirements_digitalocean
        + requirements_gcp,
        "digitalocean": requirements_base + requirements_digitalocean,
        "gcp": requirements_base + requirements_gcp,
    },
    entry_points="""
        [console_scripts]
        gluepy-cli=gluepy.commands.gluepy:cli
    """,
)
