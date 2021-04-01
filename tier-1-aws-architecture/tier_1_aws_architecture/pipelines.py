from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
from beanstalk_deploy_action import ElasticBeanStalkDeployAction


def generate_pipeline_stages(codebuild_project, role, beanstalk_application, beanstalk_environment,
                             codestar_connection):
    source_output = codepipeline.Artifact("SourceOutput")
    source_stage = codepipeline.StageProps(stage_name="Source",
                                           actions=[
                                               codepipeline_actions.BitBucketSourceAction(
                                                   connection_arn=codestar_connection.attr_connection_arn,
                                                   output=source_output,
                                                   repo="tier1",
                                                   owner="Jayvee1413",
                                                   action_name="Github",
                                                   code_build_clone_output=True,
                                                   run_order=1),
                                           ],
                                           )
    codebuild_output = codepipeline.Artifact("CodebuildOutput")
    codebuild_stage = codepipeline.StageProps(stage_name="Build",
                                              actions=[
                                                  codepipeline_actions.CodeBuildAction(
                                                      input=source_output,
                                                      project=codebuild_project,
                                                      outputs=[codebuild_output],
                                                      action_name="codebuild",
                                                      run_order=2,
                                                  )
                                              ])
    deploy_stage = codepipeline.StageProps(stage_name="Deploy",
                                           actions=[
                                               ElasticBeanStalkDeployAction(
                                                   action_name='Deploy',
                                                   role=role,
                                                   application_name=beanstalk_application.application_name,
                                                   input=codebuild_output,
                                                   environment_name=beanstalk_environment.environment_name,
                                                   run_order=3
                                               )
                                           ])
    return [source_stage, codebuild_stage, deploy_stage]


def generate_pipeline(scope, bucket, role, codebuild_project, beanstalk_application, beanstalk_environment,
                      codestar_connection):
    pipeline = codepipeline.Pipeline(scope=scope,
                                     id="CodePipelineTier1",
                                     artifact_bucket=bucket,
                                     pipeline_name="jvsantos-pipeline-tier1",
                                     role=role,
                                     stages=generate_pipeline_stages(codebuild_project=codebuild_project,
                                                                     role=role,
                                                                     beanstalk_application=beanstalk_application,
                                                                     beanstalk_environment=beanstalk_environment,
                                                                     codestar_connection=codestar_connection)
                                     )
    return pipeline
