from aws_cdk import aws_iam as iam
from policies import generate_pipeline_policy, generate_codebuild_policy


def generate_beanstalk_instance_profile_role(scope):
    role = iam.Role(scope=scope,
                    id="Tier1BeanstalkInstanceProfileRole",
                    assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                    role_name="JVSANTOSTier1BeanstalkInstanceProfileRole"
                    )
    role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSElasticBeanstalkWebTier"))
    return role


def generate_beanstalk_service_role(scope):
    role = iam.Role(scope=scope,
                    id="Tier1BeanstalkServiceRole",
                    assumed_by=iam.ServicePrincipal("elasticbeanstalk.amazonaws.com"),
                    role_name="JVSANTOSTier1BeanstalkServiceRole"
                    )

    role.add_managed_policy(
        iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSElasticBeanstalkEnhancedHealth"))
    role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSElasticBeanstalkService"))

    return role


def generate_pipeline_service_role(scope):
    role = iam.Role(scope=scope,
                    id="Tier1PipelineServiceRole",
                    assumed_by=iam.CompositePrincipal(
                        iam.ServicePrincipal("codepipeline.amazonaws.com"),
                        iam.ServicePrincipal("codebuild.amazonaws.com")))

    role.attach_inline_policy(generate_pipeline_policy(scope))
    return role


def generate_codebuild_role(scope, db_secret_arn):
    role = iam.Role(scope=scope,
                    id="Tier1CodebuildServiceRole",
                    assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"))

    role.attach_inline_policy(generate_codebuild_policy(scope, db_secret_arn=db_secret_arn))
    return role
