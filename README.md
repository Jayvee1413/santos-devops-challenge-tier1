# santos-devops-challenge-tier-1

The Cloudformation Templates are in `cfn_templates`

1. VPC Stack: `aws cloudformation deploy --template cfn_templates/JVSANTOSTier1VPCAwsArchitectureStack.json --stack-name JVSANTOSTier1VPCAwsArchitectureStack --capabilities CAPABILITY_IAM --profile <profile_name> --region ap-southeast-1`
2. Update CodeStar Connection via the AWS Console
3. Beanstalk Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier1BeanstalkAwsArchitectureStack.json --stack-name JVSANTOSTier1BeanstalkAwsArchitectureStack --capabilities CAPABILITY_NAMED_IAM --profile apper --region ap-southeast-1`
4. Beanstalk Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier1CICDAwsArchitectureStack.json --stack-name JVSANTOSTier1CICDAwsArchitectureStack --capabilities CAPABILITY_NAMED_IAM --profile apper --region ap-southeast-1`
5. Since we cannot use the generated ACM Certificate above for our Cloudfront Distribution, we would have to create a certificate in `us-east-1` region: US-East-1 ACM Certificate Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier1ACMCertificateUS-EAST-1Stack.json --stack-name JVSANTOSTier1ACMCertificateUS-EAST-1Stack  --profile apper --region us-east-1`
6. Take note of the generated ARN from `5`. (Currently: `arn:aws:acm:us-east-1:329511059546:certificate/eb486d8c-ad37-4834-bc0f-82dbb29137fd`)
7. Edit `JVSANTOSTier1CDNAwsArchitectureStack.json` line `63` for the value of the ACM Certificate generated in `5`.
8. CDN Stack: `aws cloudformation deploy --template cfn_templates\JVSANTOSTier1CDNAwsArchitectureStack.json --stack-name JVSANTOSTier1CDNAwsArchitectureStack --capabilities CAPABILITY_NAMED_IAM --profile apper --region ap-southeast-1`