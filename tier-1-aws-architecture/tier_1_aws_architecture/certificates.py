from aws_cdk import aws_certificatemanager as certificatemanager


def generate_acm_certificate(scope, hosted_zone):
    certificate = certificatemanager.Certificate(scope=scope,
                                                 id="JVSANTOSTier1ACMCertificate",
                                                 domain_name="jvsantos-tier1.apperdevops.com",
                                                 subject_alternative_names=["*.jvsantos-tier1.apperdevops.com"],
                                                 validation=certificatemanager.CertificateValidation.from_dns(
                                                     hosted_zone),
                                                 )
    return certificate
