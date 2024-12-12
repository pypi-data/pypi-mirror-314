import click

from curia.infra.databricks.deploy import deploy_databricks_tasks
from curia.infra.databricks.task import DatabricksTaskDefinition
from curia.infra.types import DatabricksTaskDeployResourceNamingConfig
from curia.infra.utils import load_tasks, describe_tasks


@click.group()
def databricks():
    pass


@databricks.command()
@click.argument("project_dir")
@click.argument("package")
@click.option("--verbose", is_flag=True, default=False, help="Toggle verbose output")
def describe(project_dir, package, verbose) -> None:
    """
    Describes all tasks
    """
    tasks = load_tasks(project_dir, package, task_type=DatabricksTaskDefinition)
    describe_tasks(tasks, verbose)


@databricks.command()
@click.argument("project_dir")
@click.argument("package")
@click.argument("prefix")
@click.argument("env")
def deploy(project_dir, package, prefix, env) -> None:
    """
    Deploys all tasks to Databricks, creating the necessary workflows and jobs in the Curia platform and in the
    Databricks workspace.
    """
    tasks = load_tasks(project_dir, package, task_type=DatabricksTaskDefinition)
    if len(tasks) == 0:
        click.echo("No tasks found")
        return
    deploy_databricks_tasks(
        tasks,
        env=env,
        resource_naming_config=DatabricksTaskDeployResourceNamingConfig(
            databricks_workflow_prefix=prefix,
            platform_task_prefix=prefix,
            platform_workflow_prefix=prefix,
        )
    )


if __name__ == "__main__":
    databricks()
