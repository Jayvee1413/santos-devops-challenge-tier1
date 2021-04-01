import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="tier_1_aws_architecture",
    version="0.0.1",

    description="Tier 1 AWS Architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "tier_1_aws_architecture"},
    packages=setuptools.find_packages(where="tier_1_aws_architecture"),

    install_requires=[
        "aws-cdk.core==1.94.1",
        "aws-cdk.aws-ec2==1.94.1",
        "aws-cdk.aws-elasticbeanstalk==1.94.1",
        "aws-cdk.aws-rds==1.94.1",
        "aws_cdk.aws-codecommit==1.94.1",
        "aws_cdk.aws-s3==1.94.1",
        "aws_cdk.aws-codebuild==1.94.1",
        "aws_cdk.aws-codepipeline==1.94.1",
        "aws_cdk.aws-s3==1.94.1",
        "aws_cdk.aws-codepipeline-actions==1.94.1",
        "aws_cdk.aws-codestarconnections==1.94.1",
        "aws_cdk.aws_route53==1.94.1",
        "aws_cdk.aws_certificatemanager==1.94.1",
        "aws_cdk.aws-cloudfront==1.94.1",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
