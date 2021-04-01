#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from tier_1_aws_architecture.tier_1_aws_architecture_stack import Tier1VPCAwsArchitectureStack, \
    Tier1BeanstalkAwsArchitectureStack, Tier1CICDAwsArchitectureStack, Tier1CDNAwsArchitectureStack

app = core.App()
account_number = os.getenv("CDK_DEFAULT_ACCOUNT")
region = os.getenv("CDK_DEFAULT_REGION")
vpc_stack = Tier1VPCAwsArchitectureStack(app, "JVSANTOSTier1VPCAwsArchitectureStack",
                                         env=core.Environment(account=account_number, region=region))
beanstalk_stack = Tier1BeanstalkAwsArchitectureStack(app, "JVSANTOSTier1BeanstalkAwsArchitectureStack", vpc_stack,
                                                     env=core.Environment(account=account_number, region=region))
cicd_stack = Tier1CICDAwsArchitectureStack(app, "JVSANTOSTier1CICDAwsArchitectureStack", beanstalk_stack, vpc_stack,
                                           env=core.Environment(account=account_number, region=region))
cdn_stack = Tier1CDNAwsArchitectureStack(app, "JVSANTOSTier1CDNAwsArchitectureStack", beanstalk_stack,
                                         env=core.Environment(account=account_number, region=region))

app.synth()
