from aws_cdk import aws_codebuild as codebuild
from aws_cdk.aws_codebuild import BuildSpec, BuildEnvironmentVariable, BuildEnvironmentVariableType


def generate_buildspec():
    buildspec = {
        "version": 0.2,
        "phases": {
            "install": {
                "runtime-versions": {
                    "nodejs": "latest"
                },
            },
            "build": {
                "commands": [
                    "echo Build started on `date`",
                    "pwd",
                    "ls",
                    "cd express-minapp/",
                    "echo HOST=$HOST >> .env",
                    "echo USERNAME=$USERNAME >> .env",
                    "echo PASSWORD=$PASSWORD >> .env",
                    "echo DATABASE=$DATABASE >> .env",
                    "npm install"
                ],
            },
            "post_build": {
                "commands": [
                    "echo Build completed on `date`"
                ]
            }
        },
        "artifacts": {
            "files": [
                "package.json",
                "src/index.js",
                "src/middlewares.js",
                "package-lock.json",
                ".env",
            ],
            "name": "express-minapp",
            "base-directory": "express-minapp"
        },
        "cache": {
            "paths": [
                "node_modules/**/*"
            ]
        }
    }

    return BuildSpec.from_object(buildspec)


def generate_codebuild_project(scope, role, db_secret):
    codebuild_project = codebuild.PipelineProject(scope=scope,
                                                  id="JVSANTOSTier1CodebuildProject",
                                                  build_spec=generate_buildspec(),
                                                  project_name="JVSANTOSTier1",
                                                  role=role,
                                                  environment=codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
                                                  environment_variables=
                                                  {
                                                      "HOST": BuildEnvironmentVariable(
                                                          value=f"{db_secret.secret_name}:host",
                                                          type=BuildEnvironmentVariableType.SECRETS_MANAGER),
                                                      "USERNAME": BuildEnvironmentVariable(
                                                          value=f"{db_secret.secret_name}:username",
                                                          type=BuildEnvironmentVariableType.SECRETS_MANAGER),
                                                      "PASSWORD": BuildEnvironmentVariable(
                                                          value=f"{db_secret.secret_name}:password",
                                                          type=BuildEnvironmentVariableType.SECRETS_MANAGER),
                                                      "DATABASE": BuildEnvironmentVariable(
                                                          value=f"{db_secret.secret_name}:dbname",
                                                          type=BuildEnvironmentVariableType.SECRETS_MANAGER),
                                                      "PORT": BuildEnvironmentVariable(
                                                          value=1337,
                                                          type=BuildEnvironmentVariableType.PLAINTEXT),
                                                  }
                                                  )

    return codebuild_project
