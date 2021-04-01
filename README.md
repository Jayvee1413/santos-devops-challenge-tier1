# santos-devops-challenge-tier-1

This project is made mainly with AWS CDK to generate the Cloudformation Templates for the Apper Devops Challenge Tier 1.
The synthesized Cloudformation templates are also included in this repository.

To run the CDK:
1. NPM should be installed
2. Install AWS CDK via `npm install aws-cdk@1.94.1`
3. Create a Python virtual environment
4. Install requirements.txt in `tier_1_aws_architecture`
5. Bootstap your AWS Account: `cdk bootstrap --profile <aws_profile>`
6. Run the following in order (while in `tier_1_aws_architecture subdirectory`:
    1. `cdk deploy JVSANTOSTier1VPCAwsArchitectureStack --profile <aws_profile>`
    2. Enable the generated CodeStar Connection in the AWS Console
    3. `cdk deploy JVSANTOSTier1BeanstalkAwsArchitectureStack --profile <aws_profile>`
    4. `cdk deploy JVSANTOSTier1CICDAwsArchitectureStack --profile <aws_profile>`
    5. `cdk deploy JVSANTOSTier1CDNAwsArchitectureStack --profile <aws_profile>`
7. If you just want to create the cloudformation templates, just run `cdk synth --profile <aws_profile> --all` 
   and the generated Cloudformation templates will be in `tier_1_aws_architecture/cdk.out`