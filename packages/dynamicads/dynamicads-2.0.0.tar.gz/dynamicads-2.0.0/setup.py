from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dynamicads",
    version="2.0.0",
    author="DynamicAds",
    author_email="support@dynamicads.dev",
    description="Official Python SDK for DynamicAds API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dynamicads/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "dataclasses>=0.6;python_version<'3.7'"
    ],
    package_data={
        "dynamicads": ["py.typed"],
    },
    zip_safe=False
)
