import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "bunny-cdk",
    "version": "0.0.0",
    "description": "bunny-cdk",
    "license": "AGPL-3.0-or-later",
    "url": "https://github.com/jlarmstrongiv/bunny-cdk.git",
    "long_description_content_type": "text/markdown",
    "author": "John L. Armstrong IV<20903247+jlarmstrongiv@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/jlarmstrongiv/bunny-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "bunny_cdk",
        "bunny_cdk._jsii"
    ],
    "package_data": {
        "bunny_cdk._jsii": [
            "bunny-cdk@0.0.0.jsii.tgz"
        ],
        "bunny_cdk": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
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
