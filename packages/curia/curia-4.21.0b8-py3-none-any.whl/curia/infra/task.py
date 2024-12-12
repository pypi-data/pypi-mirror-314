"""
Base class for creating tasks that can be run through the Curia API, with a backend of either a docker container or
a databricks job.
"""
import abc
import dataclasses
import inspect
import typing
import warnings
from typing import List, Callable, Any, Literal, Optional

from curia.infra.types import TaskType
from curia.session import Session
from curia.utils.json import sanitize

TaskIOType = Literal['literal', 'dataset', 'model', 'modelJob']


@dataclasses.dataclass
class TaskInputDefinition:
    """
    Base class for all airml-analytics input definitions, designed to interface with the AirML API
    """
    name: str
    type: TaskIOType
    optional: bool = False
    description: Optional[str] = None

    def describe(self) -> List[str]:
        """
        Describe the input definition
        :return: The description, formatted as a list of strings, with each string representing a line
        """
        return [
            f"Name: {self.name}",
            f"Type: {self.type}",
            f"Optional: {self.optional}",
            f"Description: {self.description}"
        ]


@dataclasses.dataclass
class TaskOutputDefinition:
    """
    Base class for all airml-analytics output definitions, designed to interface with the AirML API
    """
    name: str
    type: TaskIOType
    description: Optional[str] = None

    def describe(self) -> List[str]:
        """
        Describe the output definition
        :return: The description, formatted as a list of strings, with each string representing a line
        """
        return [
            f"Name: {self.name}",
            f"Type: {self.type}",
            f"Description: {self.description}"
        ]


@dataclasses.dataclass
class TaskDefinition(abc.ABC):  # pylint: disable=too-many-instance-attributes
    """
    Base class for creating and managing tasks that can be run through the Curia API, with a backend of either a
    docker container or a databricks job.
    """
    name: str
    task_slug: str
    inputs: List[TaskInputDefinition]
    outputs: List[TaskOutputDefinition]
    description: Optional[str] = None
    # while the function is optional here, it is required for the task to be run. It just gets set in the decorator.
    _function: Optional[Callable] = None  # type: ignore
    _module: Optional[str] = None
    task_type: typing.ClassVar[TaskType] = TaskType.ABSTRACT

    def __call__(self, function: Callable) -> 'TaskDefinition':  # type: ignore
        """
        Decorator to add a function to the analytics task flow definition
        :param function: The function to add
        :return: The function
        """
        self._function = function
        module = inspect.getmodule(function)
        if module is not None:
            self._module = module.__name__
        else:
            self._module = "not_found"
        return self

    @classmethod
    def get_curia_sdk(cls, api_token: str, api_endpoint: str) -> Session:
        """
        Get the Curia SDK using the provided API Key
        :param api_token:
        :param api_endpoint:
        :return:
        """
        return Session(api_token=api_token, host=api_endpoint)

    def verify_task_inputs_valid(self, task_inputs: typing.Dict[str, Any]) -> None:
        """
        Verify that the task inputs are valid by checking that all required inputs are present and that no unexpected
        inputs are present, based on the inputs defined for this task.
        :param task_inputs: The supplied task inputs to verify
        :return:
        """
        errors = []
        for defined_input in self.inputs:
            if not defined_input.optional:
                if defined_input.name not in task_inputs:
                    errors.append(f"Missing required input: {defined_input.name}")
        for actual_input in task_inputs:
            if actual_input in ['taskDefinition', 'notebook_params', 'job_id']:
                # these are special inputs that are not defined in the task definition
                continue
            if actual_input not in [i.name for i in self.inputs]:
                errors.append(f"Unexpected input: {actual_input}")

        if len(errors) > 0:
            errors_str = "\n    ".join(errors)
            raise ValueError(f"Invalid task inputs: \n    {errors_str}")

    def resolve_arguments(self, task_execution_id: str, api_token: str, api_endpoint: str) -> typing.Dict[str, Any]:
        """
        Utilize the Curia SDK to retrieve the arguments for the analytics task flow definition.
        :param task_execution_id: The task execution ID to retrieve the inputs for
        :param api_token: The Platform API token to use
        :param api_endpoint: The Platform API endpoint to use
        :return:
        """
        session = self.get_curia_sdk(api_token, api_endpoint)
        task_execution = session.api_instance.get_one_base_task_execution_controller_task_execution(
            id=task_execution_id
        )
        self.verify_task_inputs_valid(task_execution.inputs)

        resolved_dict = {}
        for task_input in self.inputs:
            if task_input.name not in task_execution.inputs:
                if task_input.optional:
                    continue
                raise ValueError(f"Missing required input: {task_input.name}")
            resolved_dict[task_input.name] = self.resolve_input(
                session,
                task_input,
                task_execution.inputs[task_input.name]
            )
        return resolved_dict

    @classmethod
    def resolve_input(cls,
                      session: Session,  # pylint: disable=unused-argument
                      task_input: TaskInputDefinition,  # pylint: disable=unused-argument
                      task_execution_value: Any) -> Any:
        """
        Resolve a single input, making additional API calls as necessary depending on the task.

        :param session: The Curia SDK session
        :param task_input: The task input definition
        :param task_execution_value: The value of the task input from the Task Execution
        :return: The resolved value
        """
        # this is a stub and will get overridden in specific contexts and environments.
        return task_execution_value

    def upload_results(self,
                       task_execution_id: str,
                       api_token: str,
                       api_endpoint: str,
                       results: typing.Dict[str, Any]) -> None:
        """
        Upload the results of the task's execution to the Curia API and S3
        :param task_execution_id: The task execution ID
        :param api_token: The API key to use to retrieve the task inputs from the Curia API
        :param api_endpoint: The API endpoint to use to retrieve the task inputs from the Curia API
        :param results: The results to upload
        :return: None
        """
        session = self.get_curia_sdk(api_token, api_endpoint)
        session.api_instance.update_one_base_task_execution_controller_task_execution(
            id=task_execution_id,
            body={
                "outputs": sanitize(results)
            }
        )

    def describe(self) -> List[str]:
        """
        Describe the task flow definition
        :return: The description, formatted as a list of strings, with each string representing a line
        """
        assert self._function is not None, "TaskDefinition must decorate a function"
        description = [
            f"Task: {self.name}",
            f"Module: {self.module}",
            f"Function: {self._function.__name__}",
            f"Description: {self.description}",
            f"Task Type: {self.task_type}",
            "Inputs:"
        ]
        for input_def in self.inputs:
            description.extend([
                "    " + line for line in input_def.describe()
            ] + [""])

        description.append("Outputs:")

        for output_def in self.outputs:
            description.extend([
                "    " + line for line in output_def.describe()
            ] + [""])

        return description

    @property
    def module(self) -> str:
        """
        The module that the task flow definition is defined in
        :return:
        """
        return typing.cast(str, self._module)

    @property
    def function_name(self) -> str:
        """
        The name of the function that the task flow definition is defined in
        :return:
        """
        return typing.cast(Callable[[Any], Any], self._function).__name__

    class Registry:
        def __init__(self):
            self._task_definitions: typing.Dict[str, TaskDefinition] = {}

        def register(self, task_definition: 'TaskDefinition') -> None:
            print(f"Registering task {task_definition.name} in module {task_definition._module}")
            if task_definition.name in self._task_definitions:
                if self._task_definitions[task_definition.name]._module != task_definition._module:
                    warnings.warn(
                        f"Task name {task_definition.name} is already registered in module "
                        f"{self._task_definitions[task_definition.name]._module}. "
                        f"Overwriting with task {task_definition.name} in module {task_definition._module}."
                    )
            self._task_definitions[task_definition.name] = task_definition

        def list(self) -> List['TaskDefinition']:
            return list(self._task_definitions.values())

    @abc.abstractmethod
    def run(self,
            task_execution_id: str,
            api_token: str,
            api_endpoint: str,
            **kwargs) -> None:
        """
        Run the analytics task flow definition
        :param task_execution_id: The task execution ID
        :param api_token: The API key to use to retrieve the task inputs from the Curia API
        :param api_endpoint: The API endpoint to use to retrieve the task inputs from the Curia API
        :param kwargs: Additional keyword arguments, specific to ContainerTaskDefinition or DatabricksTaskDefinition
        :return: The result
        """

    @abc.abstractmethod
    def build_workflow_data_block(self, inputs: List[TaskInputDefinition], task_specific_context: dict):
        pass

    @abc.abstractmethod
    def build_task_inputs(self, inputs: List[TaskInputDefinition], task_specific_context: dict):
        pass
