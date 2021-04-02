from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from aws_cdk.core import RemovalPolicy


def generate_db_secret(scope):
    secret = rds.DatabaseSecret(scope=scope,
                                id="JVSANTOSTier1RDSSecret",
                                username="tier1user",
                                )

    return secret


def generate_db_instance(scope, vpc, security_group, db_secret):
    credentials = rds.Credentials.from_secret(db_secret)

    rds_instance = rds.DatabaseInstance(scope=scope,
                                        id="JVSANTOSTier1RDS",
                                        engine=rds.DatabaseInstanceEngine.MYSQL,
                                        credentials=credentials,
                                        instance_type=ec2.InstanceType.of(
                                            ec2.InstanceClass.BURSTABLE3,
                                            ec2.InstanceSize.SMALL),
                                        vpc=vpc,
                                        security_groups=[security_group],
                                        database_name="tier1",
                                        removal_policy=RemovalPolicy.DESTROY,
                                        deletion_protection=False,
                                        multi_az=True,
                                        vpc_subnets=ec2.SubnetSelection(
                                            subnet_type=ec2.SubnetType.ISOLATED),
                                        instance_identifier="jvsantostier1rds"
                                        )
    return rds_instance
