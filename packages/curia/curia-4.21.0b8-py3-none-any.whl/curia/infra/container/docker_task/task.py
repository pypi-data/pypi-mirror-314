import importlib
import os

from curia.utils.s3 import AWSConfig


def execute() -> None:
    """
    Executes an arbitrary python ContainerTaskDefinition passed through the command line
    :return:
    """

    if os.environ.get("TASK_NAME", None) is None:
        raise ValueError("TASK_NAME envvar is required")
    if os.environ.get("TASK_MODULE", None) is None:
        raise ValueError("TASK_MODULE is required")

    # import the task
    task_module = importlib.import_module(os.environ["TASK_MODULE"])
    task = getattr(task_module, os.environ["TASK_NAME"])

    task.run(
        task_execution_id=os.environ["TASK_EXECUTION_ID"],
        api_token=os.environ["API_TOKEN"],
        api_endpoint=os.environ["API_ENDPOINT"],
        # optional parameters, mainly used for local development / testing
        aws_config=AWSConfig(
            aws_region=os.environ.get("AWS_REGION"),
            aws_endpoint_url=os.environ.get("AWS_ENDPOINT_URL"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
    )


if __name__ == "__main__":
    execute()
