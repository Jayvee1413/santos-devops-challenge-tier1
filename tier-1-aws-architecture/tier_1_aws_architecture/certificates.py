from aws_cdk import aws_certificatemanager as certificatemanager


def generate_acm_certificate(scope, hosted_zone):
    certificate = certificatemanager.Certificate(scope=scope,
                                                 id="Tier1ACMCertificate",
                                                 domain_name="jvsantos-tier1.test1.swapoop.com",
                                                 subject_alternative_names=["*.jvsantos-tier1.test1.swapoop.com"],
                                                 validation=certificatemanager.CertificateValidation.from_dns(
                                                     hosted_zone),
                                                 )
    return certificate
