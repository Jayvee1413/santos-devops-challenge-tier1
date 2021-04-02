from aws_cdk import aws_iam as iam


def generate_beanstalk_instance_profile(scope, role):
    instance_profile = iam.CfnInstanceProfile(scope=scope,
                                              id="JVSANTOSTier1BeanstalkAppInstanceProfile",
                                              roles=[role.role_name],
                                              instance_profile_name="JVSANTOSTier1BeanstalkAppInstanceProfile")
    return instance_profile
