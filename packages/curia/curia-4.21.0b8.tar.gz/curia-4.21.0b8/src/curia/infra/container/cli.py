import click

from curia.infra.container.deploy import build_container_tasks, deploy_container_tasks
from curia.infra.container.task import ContainerTaskDefinition
from curia.infra.types import ContainerTaskDeployResourceNamingConfig
from curia.infra.utils import load_tasks, describe_tasks


@click.group()
def container():
    pass


@container.command()
@click.argument("project_dir")
@click.argument("package")
@click.option("--verbose", is_flag=True, default=False, help="Toggle verbose output")
def describe(project_dir, package, verbose) -> None:
    """
    Describes all tasks
    """
    tasks = load_tasks(project_dir, package, task_type=ContainerTaskDefinition)
    if len(tasks) == 0:
        click.echo("No tasks found")
        return
    describe_tasks(tasks, verbose)


@container.command()
@click.argument("project_dir")
@click.argument("package")
@click.argument("prefix")
@click.option("--version", default="latest", help="The version to build")
@click.option("--cache-from-ecr", is_flag=True, default=False, help="Whether or not to use the ECR cache")
@click.option("--build-arg", multiple=True, help="Build arguments to pass to the docker build command")
def build(project_dir, package, prefix, version, cache_from_ecr, build_arg) -> None:
    """
    Builds all tasks
    """
    tasks = load_tasks(project_dir, package, task_type=ContainerTaskDefinition)
    if len(tasks) == 0:
        click.echo("No tasks found")
        return
    build_container_tasks(
        project_dir,
        tasks,
        resource_naming_config=ContainerTaskDeployResourceNamingConfig(
            image_prefix=prefix,
            platform_task_prefix=prefix,
            platform_workflow_prefix=prefix,
        ),
        version=version,
        cache_from_ecr=cache_from_ecr,
        build_args=build_arg,
    )


@container.command()
@click.argument("project_dir")
@click.argument("package")
@click.argument("env")
@click.argument("prefix")
@click.argument("batch_job_role")
@click.argument("ecs_task_role")
@click.argument("ecs_execution_role")
@click.option("--version", default="latest", help="The version to deploy")
@click.option("--do-build", is_flag=True,
              help="Whether or not to build the tasks before deploying")
@click.option("--build-arg", multiple=True, help="Build arguments to pass to the docker build command")
def deploy(
        project_dir,
        package,
        env,
        prefix,
        batch_job_role,
        ecs_task_role,
        ecs_execution_role,
        version,
        do_build,
        build_arg
) -> None:
    """
    Deploys all tasks
    """
    tasks = load_tasks(project_dir, package, task_type=ContainerTaskDefinition)
    if len(tasks) == 0:
        click.echo("No tasks found")
        return
    click.echo('Loaded tasks:')
    for task in tasks:
        click.echo(f'    {task.name} ({task.task_slug})')
    if do_build:
        build_container_tasks(
            project_dir,
            tasks,
            resource_naming_config=ContainerTaskDeployResourceNamingConfig(
                image_prefix=prefix,
                platform_task_prefix=prefix,
                platform_workflow_prefix=prefix,
            ),
            version=version,
            cache_from_ecr=True,
            build_args=build_arg,
        )
    deploy_container_tasks(
        tasks,
        version=version,
        env=env,
        batch_job_role=batch_job_role,
        ecs_task_role=ecs_task_role,
        ecs_execution_role=ecs_execution_role,
        resource_naming_config=ContainerTaskDeployResourceNamingConfig(
            image_prefix=prefix,
            platform_task_prefix=prefix,
            platform_workflow_prefix=prefix,
        ),
    )


if __name__ == "__main__":
    container()
