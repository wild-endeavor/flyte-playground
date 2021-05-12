import typing
from dataclasses import dataclass

from flytekit import kwtypes
from flytekit.core.context_manager import SerializationSettings
from flytekit.core.python_customized_container_task import PythonCustomizedContainerTask
from flytekit.core.shim_task import ShimTaskExecutor
from flytekit.models import task as task_models
from flytekit.core.interface import Interface


@dataclass
class FlyteCtlConfig(object):
    admin_endpoint: str
    insecure: bool = False


class FlyteCtlTask(PythonCustomizedContainerTask[FlyteCtlConfig]):
    _TASK_TYPE = "flytectl"

    def __init__(
        self,
        name: str,
        task_config: typing.Optional[FlyteCtlConfig] = None,
        **kwargs,
    ):
        if task_config is None or not task_config.admin_endpoint:
            raise ValueError("Configuration is required.")
        outputs = kwtypes(success=bool)
        super().__init__(
            name=name,
            task_config=task_config,
            container_image="flyteplayground-flytectl:123",
            executor_type=FlyteCtlTaskExecutor,
            task_type=self._TASK_TYPE,
            interface=Interface(inputs={"command": str}, outputs=outputs),
            **kwargs,
        )

    def get_custom(self, settings: SerializationSettings) -> typing.Dict[str, typing.Any]:
        return {
            "admin_endpoint": self.task_config.admin_endpoint,
            "insecure": self.task_config.insecure,
        }

    def get_command(self, settings: SerializationSettings) -> typing.List[str]:
        container_args = [
            "bash",
            "-c"
            "flytectl {{.inputs.command}} && aws --endpoint-url http://minio.flyte:9000 s3 cp /opt/true.pb {{.outputPrefix}}/outputs.pb || aws s3 cp /opt/false.pb {{.outputPrefix}}/outputs.pb",
        ]

        return container_args


class FlyteCtlTaskExecutor(ShimTaskExecutor[FlyteCtlTask]):
    def execute_from_model(self, tt: task_models.TaskTemplate, **kwargs) -> typing.Any:
        # This is a mock only and will not be what is actually run in production. In production, Flyte will run
        # the container specified in the task class above, which will call out to flytectl and run a command.
        # The output of the task will be whether or not the return code is zero.
        # Since we can't suppose any network/permissions in local execution, and since the production container
        # doesn't run Python at all, we can't supply this function with more accurate execution behavior.

        return True
