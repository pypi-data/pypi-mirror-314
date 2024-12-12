import dataclasses
from typing import ClassVar, List

from pyspark.sql import SparkSession

from curia.infra.task import TaskDefinition, TaskInputDefinition
from curia.infra.types import TaskType, DatabricksTaskCodeSourceType


@dataclasses.dataclass
class DatabricksTaskDefinition(TaskDefinition):  # pylint: disable=too-many-instance-attributes
    """
    Task definition for a task executed through a databricks job
    """
    code_src_type: DatabricksTaskCodeSourceType = DatabricksTaskCodeSourceType.S3WHEEL
    code_src_cfg: dict = dataclasses.field(default_factory=dict)
    min_workers: int = 2
    max_workers: int = 4
    task_type: ClassVar[TaskType] = TaskType.DATABRICKS

    # pylint: disable=arguments-differ
    def run(self,
            task_execution_id: str,
            api_token: str,
            api_endpoint: str,
            spark: SparkSession,
            dbutils: 'DBUtils') -> None:
        """
        Run the analytics task flow definition
        :param task_execution_id: The task execution ID
        :param api_token: The API key to use to retrieve the task inputs from the Curia API
        :param api_endpoint: The API endpoint to use to retrieve the task inputs from the Curia API
        :return: The result
        """
        assert self._function is not None, "TaskDefinition must decorate a function"
        resolved_args = self.resolve_arguments(task_execution_id, api_token, api_endpoint)
        results = self._function(**resolved_args, spark=spark, dbutils=dbutils)
        self.upload_results(task_execution_id, api_token, api_endpoint, results)

    def build_workflow_data_block(self, inputs: List[TaskInputDefinition], task_specific_context: dict):
        if "databricks_job_id" not in task_specific_context:
            raise ValueError("Databricks job ID must be provided to DatabricksTaskDefinition")
        databricks_job_id = task_specific_context["databricks_job_id"]
        return {
            "notebook_params": {
                "code_version": {
                    "required": True,
                    "descr": "Code version to use for the task"
                },
            },
            "job_id": databricks_job_id,
            **{
                task_input.name: {
                    "required": not task_input.optional,
                    "descr": task_input.description
                } for task_input in inputs
            }
        }

    def build_task_inputs(self, inputs: List[TaskInputDefinition], task_specific_context: dict):
        if "databricks_job_id" not in task_specific_context:
            raise ValueError("Databricks job ID must be provided to DatabricksTaskDefinition")
        databricks_job_id = task_specific_context["databricks_job_id"]
        return {
            "notebook_params": {
                "code_version": {
                    "required": True,
                    "descr": "Code version to use for the task"
                },
            },
            "job_id": databricks_job_id,
            **{
                task_input.name: {
                    "required": not task_input.optional,
                    "descr": task_input.description
                } for task_input in inputs
            }
        }
