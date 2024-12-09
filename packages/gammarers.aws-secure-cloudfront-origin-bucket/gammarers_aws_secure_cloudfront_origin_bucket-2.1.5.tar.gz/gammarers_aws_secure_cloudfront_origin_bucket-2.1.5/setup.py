import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "gammarers.aws-secure-cloudfront-origin-bucket",
    "version": "2.1.5",
    "description": "AWS CloudFront distribution origin S3 bucket.",
    "license": "Apache-2.0",
    "url": "https://github.com/gammarers/aws-secure-cloudfront-origin-bucket.git",
    "long_description_content_type": "text/markdown",
    "author": "yicr<yicr@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/gammarers/aws-secure-cloudfront-origin-bucket.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "gammarers.aws_secure_cloudfront_origin_bucket",
        "gammarers.aws_secure_cloudfront_origin_bucket._jsii"
    ],
    "package_data": {
        "gammarers.aws_secure_cloudfront_origin_bucket._jsii": [
            "aws-secure-cloudfront-origin-bucket@2.1.5.jsii.tgz"
        ],
        "gammarers.aws_secure_cloudfront_origin_bucket": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.156.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "gammarers.aws-secure-bucket>=2.0.14, <3.0.0",
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
