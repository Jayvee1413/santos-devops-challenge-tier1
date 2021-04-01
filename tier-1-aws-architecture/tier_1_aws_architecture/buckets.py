from aws_cdk import aws_s3 as s3


def generate_pipeline_bucket(scope):
    bucket = s3.Bucket(scope=scope,
                       id="PipelineBucket",
                       bucket_name="jvsantos-apper-pipeline-bucket-tier1"
                       )
    return bucket
