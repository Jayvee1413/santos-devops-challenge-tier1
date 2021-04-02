from aws_cdk import aws_ec2 as ec2
from aws_cdk.core import Tags


def generate_load_balancer_security_group(scope, vpc):
    sg = ec2.SecurityGroup(
        scope=scope,
        id="JVSANTOSBeanstalkApplicationLoadBalancerSG",
        description="Application Load Balancer Security Group",
        security_group_name="JVSANTOSBeanstalkApplicationLoadBalancerSG",
        vpc=vpc,
        allow_all_outbound=True
    )

    sg.add_ingress_rule(
        description="Allow HTTPS from outside",
        peer=ec2.Peer.any_ipv4(),
        connection=ec2.Port.tcp(443)
    )

    return sg


def generate_beanstalk_app_security_group(scope, vpc: ec2.Vpc, load_balancer_sg: ec2.SecurityGroup):
    sg = ec2.SecurityGroup(
        scope=scope,
        id="JVSANTOSBeanstalkApplicationSG",
        description="Beanstalk Application Security Group",
        security_group_name="JVSANTOSBeanstalkApplicationSG",
        vpc=vpc,
        allow_all_outbound=False
    )

    sg.add_ingress_rule(
        description="Allow HTTPS from load balancer",
        peer=load_balancer_sg,
        connection=ec2.Port.tcp(443)
    )
    sg.add_ingress_rule(
        description="Allow HTTP from load balancer",
        peer=load_balancer_sg,
        connection=ec2.Port.tcp(80)
    )

    sg.add_egress_rule(
        description="Outbound Rule for VPC",
        peer=ec2.Peer.ipv4(cidr_ip=vpc.vpc_cidr_block),
        connection=ec2.Port.tcp_range(start_port=1024, end_port=65535),
    )

    return sg


def generate_rds_security_group(scope, vpc: ec2.Vpc, beanstalk_app_sg: ec2.SecurityGroup):
    sg = ec2.SecurityGroup(
        scope=scope,
        id="JVSANTOSRDSSG",
        description="RDS MySQL Security Group",
        security_group_name="JVSANTOSRDSSG",
        vpc=vpc,
        allow_all_outbound=False
    )

    sg.add_ingress_rule(
        description="Allow MySQL from app",
        peer=beanstalk_app_sg,
        connection=ec2.Port.tcp(3306)
    )

    sg.add_egress_rule(
        description="Outbound Rule for VPC",
        peer=beanstalk_app_sg,
        connection=ec2.Port.tcp_range(start_port=1024, end_port=65535),
    )

    return sg
