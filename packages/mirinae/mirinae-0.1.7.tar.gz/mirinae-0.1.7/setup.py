from setuptools import setup, find_packages

setup(
    name="mirinae",
    version="0.1.7",
    description="Mirinae is a Python package for MAGO's framework",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    author="MAGO",
    author_email="galois@holamago.com",
    url="https://github.com/holamago/mirinae-cli.git",
    license="MIT",
    packages=find_packages(
        include=['mirinae', 'mirinae.utils'],
    ),
    install_requires=[
        str(r) for r in open("requirements.txt").read().split("\n") if r
    ],
    entry_points={
        "console_scripts": [
            "mirinae = mirinae.mirinae:main",  # This should be correct
        ],
    },
    include_package_data=True,
)
