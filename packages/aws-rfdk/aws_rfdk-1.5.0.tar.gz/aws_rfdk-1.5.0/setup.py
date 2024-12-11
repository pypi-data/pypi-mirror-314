import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-rfdk",
    "version": "1.5.0",
    "description": "Package for core render farm constructs",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-rfdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-rfdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_rfdk",
        "aws_rfdk._jsii",
        "aws_rfdk.deadline"
    ],
    "package_data": {
        "aws_rfdk._jsii": [
            "aws-rfdk@1.5.0.jsii.tgz"
        ],
        "aws_rfdk": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib==2.163.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.103.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<5.0.0"
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
    "scripts": [
        "src/aws_rfdk/_jsii/bin/stage-deadline"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
