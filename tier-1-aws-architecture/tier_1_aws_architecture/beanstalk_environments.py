from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticbeanstalk as beanstalk
from aws_cdk import aws_iam as iam


def generate_beanstalk_application(scope):
    app = beanstalk.CfnApplication(scope=scope,
                                   id="Tier1BeanstalkApplication",
                                   application_name="Tier1 Application")

    return app


def generate_beanstalk_environment(scope, beanstalk_app: beanstalk.CfnApplication,
                                   instance_profile: iam.CfnInstanceProfile, service_role, vpc: ec2.Vpc,
                                   instance_security_group: ec2.SecurityGroup, elb_security_group: ec2.SecurityGroup,
                                   port,
                                   certificate_arn):
    options = [beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:autoscaling:launchconfiguration",
                                                              option_name="IamInstanceProfile",
                                                              value=instance_profile.attr_arn),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:ec2:vpc",
                                                              option_name="VPCId",
                                                              value=vpc.vpc_id),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:ec2:vpc",
                                                              option_name="Subnets",
                                                              value=",".join(
                                                                  [x.subnet_id for x in vpc.private_subnets])),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:ec2:vpc",
                                                              option_name="ELBSubnets",
                                                              value=",".join(
                                                                  [x.subnet_id for x in vpc.public_subnets])),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:ec2:vpc",
                                                              option_name="DBSubnets",
                                                              value=",".join(
                                                                  [x.subnet_id for x in vpc.isolated_subnets])),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:autoscaling:launchconfiguration",
                                                              option_name="SecurityGroups",
                                                              value=instance_security_group.security_group_id),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elbv2:loadbalancer",
                                                              option_name="SecurityGroups",
                                                              value=elb_security_group.security_group_id),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elasticbeanstalk:application:environment",
                                                              option_name="PORT",
                                                              value=str(port)),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elasticbeanstalk:environment",
                                                              option_name="ServiceRole",
                                                              value=service_role.role_name),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elasticbeanstalk:environment",
                                                              option_name="EnvironmentType",
                                                              value="LoadBalanced"),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elasticbeanstalk:environment",
                                                              option_name="LoadBalancerType",
                                                              value="application"),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:ec2:instances",
                                                              option_name="InstanceTypes",
                                                              value="t3.micro"),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elbv2:listenerrule:default",
                                                              option_name="PathPatterns",
                                                              value="/**/*"),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elasticbeanstalk:healthreporting:system",
                                                              option_name="SystemType",
                                                              value="enhanced"),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:autoscaling:asg",
                                                              option_name="MinSize",
                                                              value="2"),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:autoscaling:asg",
                                                              option_name="MaxSize",
                                                              value="4"),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elbv2:listener:443",
                                                              option_name="ListenerEnabled",
                                                              value="true"),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elbv2:listener:443",
                                                              option_name="Protocol",
                                                              value="HTTPS"),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elbv2:listener:443",
                                                              option_name="SSLCertificateArns",
                                                              value=certificate_arn),

               beanstalk.CfnEnvironment.OptionSettingProperty(
                   namespace="aws:elasticbeanstalk:environment:process:default",
                   option_name="Port",
                   value=str(port)),
               beanstalk.CfnEnvironment.OptionSettingProperty(namespace="aws:elasticbeanstalk:application",
                                                              option_name="Application Healthcheck URL",
                                                              value=f"HTTP:{str(port)}/"),

               ]

    environment = beanstalk.CfnEnvironment(scope=scope,
                                           id="BeanstalkEnvironment",
                                           environment_name="Tier1-Environment",
                                           application_name=beanstalk_app.application_name,
                                           solution_stack_name="64bit Amazon Linux 2 v5.3.0 running Node.js 14",
                                           option_settings=options,
                                           )
    return environment
