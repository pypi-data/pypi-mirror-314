import dataclasses
from enum import Enum


@dataclasses.dataclass(frozen=True)
class TaskDeployResourceNamingConfig:
    platform_task_prefix: str
    platform_workflow_prefix: str


@dataclasses.dataclass(frozen=True)
class ContainerTaskDeployResourceNamingConfig(TaskDeployResourceNamingConfig):
    image_prefix: str


@dataclasses.dataclass(frozen=True)
class DatabricksTaskDeployResourceNamingConfig(TaskDeployResourceNamingConfig):
    databricks_workflow_prefix: str


class TaskType(Enum):
    """
    Enum for the different types of tasks. Should match the types defined in type.setter in
    curia/api/swagger_client/models/task.py, along with an Abstract type that specifies that the task
    is not a concrete task type, but rather a base class for other task types.
    """
    ABSTRACT = "Abstract"
    DATAQUERY = "DataQuery"
    CONTAINER = "ContainerExecution"
    DATABRICKS = "DatabricksJob"


class DatabricksTaskCodeSourceType(Enum):
    """
    Enum for the different types of code sources for databricks tasks. Currently supports S3WHEEL, PRIVATE_PYPI
    """
    S3WHEEL = "S3WHEEL"
    PRIVATE_PYPI = "PRIVATE_PYPI"

