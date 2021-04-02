# santos-devops-challenge-tier-1

The Cloudformation Templates are in `cfn_templates`

1. VPC Stack: `aws cloudformation deploy --template cfn_templates/JVSANTOSTier1VPCAwsArchitectureStack.json --stack-name JVSANTOSTier1VPCAwsArchitectureStack --capabilities CAPABILITY_IAM --profile <profile_name> --region ap-southeast-1`
2. Update CodeStar Connection via the AWS Console
3. Beanstalk Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier1BeanstalkAwsArchitectureStack.json --stack-name JVSANTOSTier1BeanstalkAwsArchitectureStack --capabilities CAPABILITY_NAMED_IAM --profile apper --region ap-southeast-1`
4. Beanstalk Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier1CICDAwsArchitectureStack.json --stack-name JVSANTOSTier1CICDAwsArchitectureStack --capabilities CAPABILITY_NAMED_IAM --profile apper --region ap-southeast-1`
5. CDN Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier1CDNAwsArchitectureStack.json --stack-name JVSANTOSTier1CDNAwsArchitectureStack --capabilities CAPABILITY_NAMED_IAM --profile apper --region ap-southeast-1`