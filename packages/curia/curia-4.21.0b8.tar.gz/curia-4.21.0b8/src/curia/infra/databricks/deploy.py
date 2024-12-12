"""
This script deploys container tasks defined in airml_analytics
"""
import base64
import json
import os

import click
import databricks.sdk.service.compute as databricks_compute
import databricks.sdk.service.jobs as databricks_jobs
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ExportFormat
from typing import List

from curia.infra.common import update_curia_task_and_stub_workflow
from curia.infra.databricks.task import DatabricksTaskDefinition
from curia.infra.types import DatabricksTaskDeployResourceNamingConfig, DatabricksTaskCodeSourceType


def deploy_databricks_tasks(
        tasks: List[DatabricksTaskDefinition],
        env: str,
        resource_naming_config: DatabricksTaskDeployResourceNamingConfig
) -> None:
    """
    Deploys all tasks as databricks jobs
    :param tasks: List of tasks to deploy
    :param env: The environment to deploy to
    :param resource_naming_config: The resource naming config to use
    :return:
    """
    db_client = WorkspaceClient(
        host=os.environ["DATABRICKS_HOST"],
        token=os.environ["DATABRICKS_TOKEN"]
    )
    for task in tasks:
        databricks_job_id = create_or_update_databricks_job(
            task,
            env,
            db_client,
            resource_naming_config=resource_naming_config
        )
        update_curia_task_and_stub_workflow(
            task,
            env,
            resource_naming_config=resource_naming_config,
            task_specific_context={
                "databricks_job_id": databricks_job_id
            }
        )
        click.echo(f"Deployed {task.task_slug} to {env}")


def create_or_update_databricks_job(
        task: DatabricksTaskDefinition,
        env: str,
        db_client: WorkspaceClient,
        resource_naming_config: DatabricksTaskDeployResourceNamingConfig):
    """
    Creates or updates a databricks job in the Databricks workspace, configuring it to run the task with access to
    appropriate S3 resources and the correct cluster configuration.
    """
    databricks_task_name = f"{resource_naming_config.databricks_workflow_prefix}{env}-{task.task_slug}"
    notebook_path = _create_databricks_notebook(
        task,
        env,
        db_client,
        databricks_task_name
    )
    kwargs = dict(
        name=databricks_task_name,
        tasks=[
            databricks_jobs.Task(
                description="",
                existing_cluster_id="",
                notebook_task=databricks_jobs.NotebookTask(
                    base_parameters={
                        "GENERICS_ONLY": "false",
                        "code_version": "NA",
                        "data_version": "NA",
                        "env": "PROD",
                    },
                    notebook_path=notebook_path,
                    source=databricks_jobs.Source.WORKSPACE
                ),
                task_key="job",
                new_cluster=databricks_compute.ClusterSpec(
                    autoscale=databricks_compute.AutoScale(
                        max_workers=task.max_workers,
                        min_workers=task.min_workers
                    ),
                    aws_attributes=databricks_compute.AwsAttributes(
                        first_on_demand=1,
                        availability=databricks_compute.AwsAvailability.SPOT_WITH_FALLBACK,
                        zone_id="us-east-1c",
                        instance_profile_arn="arn:aws:iam::452233835093:instance-profile/Databricks-S3-prod",
                        spot_bid_price_percent=100,
                        ebs_volume_count=0
                    ),
                    spark_version="9.1.x-scala2.12",
                    spark_conf={
                        "spark.hadoop.fs.s3a.acl.default": "BucketOwnerFullControl",
                        "spark.sql.shuffle.partitions": "200",
                        "spark.sql.legacy.timeParserPolicy": "LEGACY",
                        "spark.sql.legacy.parquet.datetimeRebaseModeInWrite": "LEGACY"
                    },
                    node_type_id="i3.2xlarge",
                    driver_node_type_id="i3.4xlarge",
                    ssh_public_keys=[],
                    custom_tags={},
                    spark_env_vars={},
                    enable_elastic_disk=True,
                    cluster_source=databricks_compute.ClusterSource.JOB,
                    enable_local_disk_encryption=False,
                    runtime_engine=databricks_compute.RuntimeEngine.STANDARD
                )
            )
        ],
    )
    # check if job exists
    jobs = db_client.jobs.list(name=databricks_task_name)
    jobs_list = list(jobs)
    job = None
    if len(jobs_list) > 1:
        for job in jobs_list[:-1]:
            click.echo(f"Deleting excess job {job.job_id}")
            db_client.jobs.delete(job_id=job.job_id)
        job = jobs_list[-1]
    elif len(jobs_list) == 1:
        job = jobs_list[0]

    if job is not None:
        click.echo(f"Job {databricks_task_name} exists, updating")
        db_client.jobs.reset(job_id=job.job_id, new_settings=databricks_jobs.JobSettings(**kwargs))

    else:
        click.echo(f"Job {databricks_task_name} doesn't exist, creating")
        job = db_client.jobs.create(**kwargs)
    return job.job_id


def _build_cell(code: str):
    """
    Builds a databricks notebook cell from a string of code
    """
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [line + "\n" for line in code.split("\n")],
        "outputs": []
    }


def _build_notebook(cells: List[dict]):
    """
    Builds a databricks notebook from a list of cells
    """
    return {
        "cells": cells,
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 0
    }


def _build_task_head_notebook(env: str, task: DatabricksTaskDefinition, curia_api_endpoint: str):
    """
    Creates a notebook for the task head, which is responsible for setup surrounding the code execution and
    calling the task code.
    """
    cells = []

    package = task.code_src_cfg["package"]
    if "package" not in task.code_src_cfg:
        raise ValueError("package not specified in code_src_cfg")

    install_cell = _build_install_cell(task, package)

    cells.append(install_cell)
    cells.append(_build_cell(f"""
import {package}

print({package}.__version__)
"""))

    cells.append(_build_cell(f"""
from {task.module} import {task.function_name}
""".strip()))

    cells.append(_build_cell(f"""
environment = "{env}"
execution_id = dbutils.widgets.get("executionId")
api_token = dbutils.secrets.get("airml-etl", "curia-{env}-api-token")
api_endpoint = "{curia_api_endpoint}"
""".strip()))

    cells.append(_build_cell(f"""
{task.function_name}.run(
    task_execution_id=execution_id,
    api_token=api_token,
    api_endpoint=api_endpoint,
    spark=spark,
    dbutils=dbutils
)
""".strip()))
    return _build_notebook(cells)


def _build_install_cell(task, package):
    if task.code_src_type == DatabricksTaskCodeSourceType.S3WHEEL:
        return _build_install_cell_s3wheel(task, package)
    if task.code_src_type == DatabricksTaskCodeSourceType.PRIVATE_PYPI:
        return _build_install_cell_private_pipy(package)
    raise ValueError(f"Unsupported code_src_type {task.code_src_type}")


def _build_install_cell_s3wheel(task, package):
    if "bucket" not in task.code_src_cfg:
        raise ValueError("bucket not specified in code_src_cfg")
    bucket = task.code_src_cfg["bucket"]
    install_cell = _build_cell(f"""
code_version = dbutils.widgets.get("code_version")
import boto3

client = boto3.client("s3")

client.download_file("{bucket}", f"{package}-{{code_version}}-py3-none-any.whl", f"/dbfs/{package}-{{code_version}}-py3-none-any.whl")

%pip install /dbfs/{package}-$code_version-py3-none-any.whl
    """.strip())
    return install_cell


def _build_install_cell_private_pipy(package):
    install_cell = _build_cell(f"""
code_version = dbutils.widgets.get("code_version")

PRIVATE_PYPI_USERNAME = dbutils.secrets.get(scope="airml-etl", key="PRIVATE_PYPI_USERNAME")
PRIVATE_PYPI_PASSWORD = dbutils.secrets.get(scope="airml-etl", key="PRIVATE_PYPI_PASSWORD")

%pip install --index-url=https://$PRIVATE_PYPI_USERNAME:$PRIVATE_PYPI_PASSWORD@pypi.curia.ai/ {package}==$code_version
    """.strip())
    return install_cell


def _create_databricks_notebook(
        task: DatabricksTaskDefinition,
        env: str,
        db_client: WorkspaceClient,
        databricks_task_name: str):
    """
    Builds a databricks notebook for a task using the task definition and deploys that notebook to the databricks
    workspace.

    :param task: The task definition
    :param env: The environment to deploy to
    :param db_client: The databricks workspace client
    :param databricks_task_name: The name of the task
    """
    notebook = _build_task_head_notebook(env, task, os.environ["CURIA_API_ENDPOINT"])
    try:
        db_client.workspace.mkdirs(f"/etl/{env}")
    except Exception:
        # already exists
        pass
    notebook_path = f"/etl/{env}/{databricks_task_name}"
    db_client.workspace.import_(
        path=notebook_path,
        format=ExportFormat.JUPYTER,
        content=base64.b64encode(json.dumps(notebook).encode("utf-8")).decode("utf-8"),
        overwrite=True
    )
    return notebook_path
