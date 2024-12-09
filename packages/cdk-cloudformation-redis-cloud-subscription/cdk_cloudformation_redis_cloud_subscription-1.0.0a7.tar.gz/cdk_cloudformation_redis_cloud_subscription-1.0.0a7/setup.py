import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cloudformation-redis-cloud-subscription",
    "version": "1.0.0.a7",
    "description": "CloudFormation template for Pro Subscription.",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-cloudformation.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-cloudformation.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudformation_redis_cloud_subscription",
        "cdk_cloudformation_redis_cloud_subscription._jsii"
    ],
    "package_data": {
        "cdk_cloudformation_redis_cloud_subscription._jsii": [
            "redis-cloud-subscription@1.0.0-alpha.7.jsii.tgz"
        ],
        "cdk_cloudformation_redis_cloud_subscription": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.171.1, <3.0.0",
        "constructs>=10.4.2, <11.0.0",
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
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
