import jsii
from aws_cdk import (
    aws_codepipeline as codepipeline,
    core
)
from aws_cdk.aws_codepipeline import IAction


class ElasticBeanStalkDeployActionProps(codepipeline.CommonAwsActionProps):

    @property
    def environment_name(self):
        return self._environment_name

    @property
    def application_name(self):
        return self._application_name

    @property
    def role(self):
        return self._role

    def __init__(self, *, environment_name, application_name, role) -> None:
        self._environment_name = environment_name
        self._application_name = application_name
        self._role = role


@jsii.implements(IAction)
class ElasticBeanStalkDeployAction:

    @property
    def props(self) -> ElasticBeanStalkDeployActionProps:
        return self._props

    @property
    def action_properties(self) -> codepipeline.ActionProperties:
        return self._action_properties

    @action_properties.setter
    def action_properties(self, value):
        self._action_properties = value

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        self._props = ElasticBeanStalkDeployActionProps(
            application_name=kwargs['application_name'],
            environment_name=kwargs['environment_name'],
            role=kwargs['role']
        )
        self._action_properties = codepipeline.ActionProperties(
            provider="ElasticBeanstalk",
            category=codepipeline.ActionCategory.DEPLOY,
            inputs=[kwargs['input']],
            action_name=kwargs['action_name'],
            role=kwargs['role'],
            artifact_bounds=codepipeline.ActionArtifactBounds(
                max_inputs=1,
                max_outputs=0,
                min_inputs=1,
                min_outputs=0
            )
        )

    def bind(self, scope: core.Construct, stage: codepipeline.IStage,
             options: codepipeline.ActionBindOptions) -> codepipeline.ActionConfig:
        return codepipeline.ActionConfig(
            configuration={
                'ApplicationName': self.props.application_name,
                'EnvironmentName': self.props.environment_name

            }
        )

    def on_state_change(self, name, target=None, *, description=None, enabled=None, event_bus=None, event_pattern=None,
                        rule_name=None, schedule=None, targets=None):
        pass
