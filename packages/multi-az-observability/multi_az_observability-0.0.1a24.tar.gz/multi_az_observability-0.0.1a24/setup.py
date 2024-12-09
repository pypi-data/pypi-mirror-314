import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "multi_az_observability",
    "version": "0.0.1.a24",
    "description": "A construct for implementing multi-AZ observability to detect single AZ impairments",
    "license": "MIT",
    "url": "https://github.com/bamcis-io/multi-az-observability",
    "long_description_content_type": "text/markdown",
    "author": "Michael Haken<michael.haken@outlook.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/bamcis-io/multi-az-observability"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "multi_az_observability",
        "multi_az_observability._jsii"
    ],
    "package_data": {
        "multi_az_observability._jsii": [
            "multi-az-observability@0.0.1-alpha.24.jsii.tgz"
        ],
        "multi_az_observability": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.138.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.105.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
