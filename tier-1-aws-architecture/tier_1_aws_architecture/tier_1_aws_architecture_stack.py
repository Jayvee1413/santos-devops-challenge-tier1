from aws_cdk import core as cdk, core

from aws_cdk.core import Tags
from beanstalk_environments import generate_beanstalk_application, generate_beanstalk_environment
from buckets import generate_pipeline_bucket
from certificates import generate_acm_certificate
from cloudfront_distributions import generate_cloudfront_distribution
from codebuilds import generate_codebuild_project
from codestar_connections import generate_codestar_connection
from databases import generate_db_secret, generate_db_instance
from hosted_zones import generate_lookedup_hosted_zone, generate_record_in_hosted_zone
from instance_profiles import generate_beanstalk_instance_profile
from nacls import generate_public_nacl, generate_private_nacl, generate_isolated_nacl
from pipelines import generate_pipeline
from roles import generate_beanstalk_instance_profile_role, generate_beanstalk_service_role, \
    generate_pipeline_service_role, generate_codebuild_role
from security_groups import generate_load_balancer_security_group, generate_beanstalk_app_security_group, \
    generate_rds_security_group
from vpcs import generate_vpc


class Tier1VPCAwsArchitectureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC Creation
        self.vpc = generate_vpc(scope=self)

        # NACLs Creation
        generate_public_nacl(scope=self, vpc=self.vpc)
        generate_private_nacl(scope=self, vpc=self.vpc)
        generate_isolated_nacl(scope=self, vpc=self.vpc, private_subnets=self.vpc.private_subnets)

        # Generate CodeStar Connection

        self.codestar_connection = generate_codestar_connection(scope=self)

        # RDS Creation
        # Security Group Creation
        self.load_balancer_security_group = generate_load_balancer_security_group(scope=self, vpc=self.vpc)
        self.beanstalk_app_security_group = generate_beanstalk_app_security_group(scope=self,
                                                                                  vpc=self.vpc,
                                                                                  load_balancer_sg=self.load_balancer_security_group)
        rds_security_group = generate_rds_security_group(scope=self, vpc=self.vpc,
                                                         beanstalk_app_sg=self.beanstalk_app_security_group)

        # RDS
        self.db_secret = generate_db_secret(scope=self)
        generate_db_instance(scope=self, vpc=self.vpc, security_group=rds_security_group, db_secret=self.db_secret)
        # Hosted Zone and ACM Certificate

        self.hosted_zone = generate_lookedup_hosted_zone(scope=self)
        self.acm_certificate = generate_acm_certificate(scope=self, hosted_zone=self.hosted_zone)
        Tags.of(scope).add("Application", "JVSANTOSTier1")


class Tier1BeanstalkAwsArchitectureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc_stack = vpc_stack
        vpc = self.vpc_stack.vpc

        # Roles Creation
        beanstalk_instance_profile_role = generate_beanstalk_instance_profile_role(scope=self)
        beanstalk_service_role = generate_beanstalk_service_role(scope=self)
        instance_profile = generate_beanstalk_instance_profile(scope=self, role=beanstalk_instance_profile_role)

        # Beanstalk Creation
        self.beanstalk_application = generate_beanstalk_application(scope=self)
        self.beanstalk_environment = generate_beanstalk_environment(scope=self,
                                                                    beanstalk_app=self.beanstalk_application,
                                                                    instance_profile=instance_profile,
                                                                    service_role=beanstalk_service_role,
                                                                    vpc=vpc,
                                                                    instance_security_group=self.vpc_stack.beanstalk_app_security_group,
                                                                    elb_security_group=self.vpc_stack.load_balancer_security_group,
                                                                    port=1337,
                                                                    certificate_arn=self.vpc_stack.acm_certificate.certificate_arn
                                                                    )

        self.beanstalk_environment.add_depends_on(self.beanstalk_application)

        core.CfnOutput(
            scope=self, id="EBURL", value=self.beanstalk_environment.attr_endpoint_url
        )

        Tags.of(scope).add("Application", "JVSANTOSTier1")


class Tier1CICDAwsArchitectureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, beanstalk_stack, vpc_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Bucket creation
        pipeline_bucket = generate_pipeline_bucket(scope=self)

        # Pipeline Creation
        pipeline_service_role = generate_pipeline_service_role(scope=self)
        codebuild_role = generate_codebuild_role(scope=self, db_secret_arn=vpc_stack.db_secret.secret_full_arn)

        # Codebuild Project Creation
        codebuild_project = generate_codebuild_project(scope=self, db_secret=vpc_stack.db_secret, role=codebuild_role)

        generate_pipeline(scope=self, bucket=pipeline_bucket, role=pipeline_service_role,
                          codebuild_project=codebuild_project,
                          beanstalk_environment=beanstalk_stack.beanstalk_environment,
                          beanstalk_application=beanstalk_stack.beanstalk_application,
                          codestar_connection=vpc_stack.codestar_connection)


class Tier1CDNAwsArchitectureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, beanstalk_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        core.CfnOutput(
            scope=self, id="EBURL", value=beanstalk_stack.beanstalk_environment.attr_endpoint_url
        )

        cloudfront_distribution = generate_cloudfront_distribution(scope=self,
                                                                   certificate=beanstalk_stack.vpc_stack.acm_certificate,
                                                                   beanstalk_url=beanstalk_stack.beanstalk_environment.attr_endpoint_url)
        generate_record_in_hosted_zone(scope=self, hosted_zone=beanstalk_stack.vpc_stack.hosted_zone,
                                       cloudfront_distribution=cloudfront_distribution)
