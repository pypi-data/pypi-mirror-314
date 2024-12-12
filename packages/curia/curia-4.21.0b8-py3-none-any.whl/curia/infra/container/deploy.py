"""
This script deploys container tasks defined in airml_analytics
"""
import base64
import os
import pkgutil
import warnings
from typing import Optional, List, Tuple

import boto3
import click
import docker
from docker.errors import ImageNotFound, DockerException, BuildError, APIError

from curia.infra.common import update_curia_task_and_stub_workflow
from curia.infra.exceptions import TaskBuildError
from curia.infra.task import TaskDefinition
from curia.infra.types import ContainerTaskDeployResourceNamingConfig


def build_container_tasks(
        project_dir: str,
        tasks: List[TaskDefinition],
        version: str,
        resource_naming_config: ContainerTaskDeployResourceNamingConfig,
        build_args: Optional[List[List[str]]] = None,
        cache_from_ecr: bool = False) -> None:
    """
    Builds all tasks as docker containers
    :param project_dir: Project directory
    :param tasks: List of tasks to build
    :param version: Version to tag the docker containers with
    :param resource_naming_config: Resource naming config
    :param build_args: List of build args to pass to docker
    :param cache_from_ecr: If true, will pull the latest version of the task from ECR before building and use that
        as the cache and prep the task for deployment to ECR
    :return:
    """
    try:
        docker_client = docker.from_env()
    except DockerException as exception:
        raise TaskBuildError(f"Could not connect to docker: {exception}. Is docker running?") from exception

    if cache_from_ecr:
        # If we are caching from ECR, we need to login to ECR first
        # the images locally
        docker_client, base_ecr_uri = _login_to_docker_registries(docker_client)
    else:
        base_ecr_uri = None

    for task in tasks:
        _build_container_task(
            project_dir,
            task,
            version,
            base_ecr_uri=base_ecr_uri,
            build_args=build_args,
            docker_client=docker_client,
            resource_naming_config=resource_naming_config
        )


def deploy_container_tasks(
        tasks: List[TaskDefinition],
        version: str,
        env: str,
        ecs_task_role: str,
        ecs_execution_role: str,
        batch_job_role: str,
        resource_naming_config: ContainerTaskDeployResourceNamingConfig
) -> None:
    """
    Deploys all tasks as docker containers
    :param tasks: List of tasks to deploy
    :param version: The version to label the deployed containers with
    :param env: The environment to deploy to
    :param ecs_task_role: The role to use for the ECS tasks
    :param ecs_execution_role: The role to use for the ECS execution
    :param batch_job_role: The role to use for the batch jobs
    :param resource_naming_config: The resource naming config to use
    :return:
    """
    docker_client, base_ecr_uri = _login_to_docker_registries(docker.from_env())
    for task in tasks:
        _push_container_to_ecr(
            task,
            docker_client=docker_client,
            version=version,
            base_ecr_uri=base_ecr_uri,
            resource_naming_config=resource_naming_config
        )
        ecs_task_family = _update_ecs_task_definition(
            task,
            env,
            base_ecr_uri,
            version,
            ecs_task_role,
            ecs_execution_role,
            resource_naming_config=resource_naming_config
        )
        _update_batch_job_definition(
            task,
            env,
            batch_job_role,
            base_ecr_uri,
            version,
            resource_naming_config=resource_naming_config
        )
        update_curia_task_and_stub_workflow(
            task,
            env,
            resource_naming_config=resource_naming_config,
            task_specific_context={
                "ecs_task_family": ecs_task_family
            }
        )


def get_boto3_client(service):
    additional_kwargs = {}
    if 'AWS_DEFAULT_REGION' in os.environ:
        additional_kwargs['region_name'] = os.environ['AWS_DEFAULT_REGION']
    if 'AWS_ENDPOINT_URL' in os.environ:
        additional_kwargs['endpoint_url'] = os.environ['AWS_ENDPOINT_URL']
    if 'AWS_ACCESS_KEY_ID' in os.environ:
        additional_kwargs['aws_access_key_id'] = os.environ['AWS_ACCESS_KEY_ID']
    if 'AWS_SECRET_ACCESS_KEY' in os.environ:
        additional_kwargs['aws_secret_access_key'] = os.environ['AWS_SECRET_ACCESS_KEY']
    return boto3.client(
        service
    )


def _create_docker_build_directory(project_dir: str) -> str:
    try:
        file_binary = pkgutil.get_data('curia', 'infra/container/docker_task/Dockerfile')
        # create build directory
        os.makedirs(os.path.join(project_dir, "build"), exist_ok=True)
        with open(os.path.join(project_dir, "build/Dockerfile"), "wb") as f:
            f.write(file_binary)

        task_binary = pkgutil.get_data('curia', 'infra/container/docker_task/task.py')
        with open(os.path.join(project_dir, "build/task.py"), "wb") as f:
            f.write(task_binary)
    except PermissionError as e:
        raise TaskBuildError("Could not create or write to docker build directory: " + str(e)) from e

    return "build/"


def _teardown_docker_build_directory(project_dir) -> None:
    os.remove(os.path.join(project_dir, "build/Dockerfile"))
    os.remove(os.path.join(project_dir, "build/task.py"))
    os.rmdir(os.path.join(project_dir, "build"))


def _build_container_task(
        project_dir: str,
        task: TaskDefinition,
        version: str,
        docker_client: docker.DockerClient,
        resource_naming_config: ContainerTaskDeployResourceNamingConfig,
        base_ecr_uri: Optional[str] = None,
        build_args: Optional[List[List[str]]] = None) -> None:
    """
    Builds a container task
    :param project_dir: The project directory to deploy
    :param task: The task to deploy
    :param version: The version of the task to deploy
    :param docker_client: The docker client to use
    :param resource_naming_config: The resource naming config to use
    :param base_ecr_uri: The base ECR URI to push to
    :param build_args: A list of build arguments to passed to the buildargs of the docker build command
    :return:
    """
    click.echo(f"Building {task.name} version {version}")
    if build_args is None:
        build_args = []
    # build the docker image

    arguments = {}

    tags = []

    if base_ecr_uri is not None:
        repository_name = f"{resource_naming_config.image_prefix}{task.task_slug}"
        pull_repository_name = f"{base_ecr_uri}/{repository_name}"
        tags.append(f"{pull_repository_name}:latest")
        tags.append(f"{pull_repository_name}:{version}")
        # pull the latest image from ECR
        try:
            docker_client.images.pull(
                repository=pull_repository_name,
                tag="latest"
            )
            arguments["cache_from"] = [f"{pull_repository_name}:latest"]
        except ImageNotFound:
            warnings.warn(f"Could not find image {pull_repository_name}:LATEST, building from scratch")
        except APIError as e:
            warnings.warn(f"Could not pull image {pull_repository_name}:LATEST, building from scratch: {e}")

    _create_docker_build_directory(project_dir)

    try:
        image, _ = docker_client.images.build(
            path=project_dir,
            dockerfile=os.path.join(project_dir, "build/Dockerfile"),
            buildargs={
                "TASK_NAME": task.function_name,
                "TASK_MODULE": task.module,
                **{arg[0]: arg[1] for arg in build_args}
            },
            **arguments,
            tag=task.task_slug,
        )
    except BuildError as e:
        click.echo("BUILD ERROR: ")
        for line in e.build_log:
            if 'stream' in line:
                click.echo(line['stream'].strip())
            else:
                click.echo(line)
        raise TaskBuildError(f"Could not build image for task {task.name}") from e
    except Exception as e:
        click.echo(f"DOCKER ERROR: {e}")
        raise TaskBuildError(f"Could not build image for task {task.name}") from e
    finally:
        _teardown_docker_build_directory(project_dir)
    click.echo(f"Built {task.name} version {version}")

    for tag in tags:
        image.tag(tag)

    click.echo(f"Tagged {task.name} version {version}")


def _push_container_to_ecr(task: TaskDefinition,
                           version: str,
                           docker_client: docker.DockerClient,
                           resource_naming_config: ContainerTaskDeployResourceNamingConfig,
                           base_ecr_uri: Optional[str] = None) -> None:
    """
    Pushes a single task to ECR
    :param task: The task to push
    :param version: The version of the task to push
    :param docker_client: The docker client to use
    :param resource_naming_config: The resource naming config to use
    :param base_ecr_uri: The base ECR URI to push to
    :return:
    """
    click.echo(f"Pushing {task.name} version {version}")
    if base_ecr_uri is None:
        raise ValueError("base_ecr_uri is required when pushing to ECR")

    # check if ecr repository exists
    # if not, create it
    client = get_boto3_client("ecr")
    repository_name = f"{resource_naming_config.image_prefix}{task.task_slug}"
    try:
        client.describe_repositories(repositoryNames=[repository_name])
    except client.exceptions.RepositoryNotFoundException:
        client.create_repository(repositoryName=repository_name)

    # push the image
    resp = docker_client.images.push(
        repository=f"{base_ecr_uri}/{repository_name}",
        tag="latest"
    )
    click.echo(resp)
    resp = docker_client.images.push(
        repository=f"{base_ecr_uri}/{repository_name}",
        tag=version
    )
    click.echo(resp)


def _update_batch_job_definition(task: TaskDefinition,
                                 stage: str,
                                 batch_job_role: str,
                                 base_ecr_uri: str,
                                 version: str,
                                 resource_naming_config: ContainerTaskDeployResourceNamingConfig) -> None:
    """
    Creates or updates the batch job definition for a task
    :param task: The task to create or update the batch job definition for
    :param stage: The stage to create or update the batch job definition for
    :param batch_job_role: The ARN of the batch job role
    :param base_ecr_uri: The base ECR URI
    :param version: The version of the task to use
    :param resource_naming_config:
    """
    definition = {
        "jobDefinitionName": f"{resource_naming_config.image_prefix}{stage}-{task.task_slug}",
        "type": "container",
        "containerProperties": {
            "image": f"{base_ecr_uri}/{resource_naming_config.image_prefix}{task.task_slug}:{version}",
            "vcpus": 16,
            "memory": 64000,
            "volumes": [],
            "environment": [
                {
                    "name": "STAGE"
                },
                {
                    "name": "PROCESS_JOB_ID"
                }
            ],
            "mountPoints": [],
            "ulimits": [],
            "jobRoleArn": batch_job_role,
            "command": [
                "python",
                "task.py"
            ]
        }
    }
    client = get_boto3_client("batch")
    try:
        client.register_job_definition(**definition)
    except client.exceptions.ClientException as exception:
        raise TaskBuildError(f"Could not create or update task definition for {task.name}: {exception}") from exception


def _update_ecs_task_definition(task: TaskDefinition,  # pylint: disable=too-many-arguments
                                stage: str,
                                base_ecr_uri: str,
                                version: str,
                                ecs_task_role: str,
                                ecs_execution_role: str,
                                resource_naming_config: ContainerTaskDeployResourceNamingConfig) -> str:
    """
    Creates or updates the ECS task definition for a task
    :param task:
    :param stage:
    :param base_ecr_uri:
    :param version:
    :param ecs_task_role:
    :param ecs_execution_role:
    :param resource_naming_config:
    :return: ECS task definition family
    """
    ecs_task_family = f"{resource_naming_config.image_prefix}{stage}-{task.task_slug}"

    definition = {
        "family": ecs_task_family,
        "containerDefinitions": [
            {
                "name": "main",
                "image": f"{base_ecr_uri}/{resource_naming_config.image_prefix}{task.task_slug}:{version}",
                "cpu": 0,
                "portMappings": [
                    {
                        "containerPort": 80,
                        "hostPort": 80,
                        "protocol": "tcp"
                    },
                    {
                        "containerPort": 443,
                        "hostPort": 443,
                        "protocol": "tcp"
                    }
                ],
                "essential": True,
                "environment": [],
                "mountPoints": [],
                "volumesFrom": [],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-create-group": "true",
                        "awslogs-group": f"/ecs/{resource_naming_config.image_prefix}{stage}-{task.task_slug}",
                        "awslogs-region": "us-east-1",
                        "awslogs-stream-prefix": "ecs"
                    }
                }
            }
        ],
        "executionRoleArn": ecs_execution_role,
        "taskRoleArn": ecs_task_role,
        "networkMode": "awsvpc",
        "requiresCompatibilities": [
            "FARGATE"
        ],
        "cpu": "16384",
        "memory": "65536"
    }
    client = get_boto3_client("ecs")
    try:
        client.register_task_definition(**definition)
    except client.exceptions.ClientException as exception:
        raise TaskBuildError(f"Could not create or update task definition for {task.name}: {exception}") from exception
    return ecs_task_family


def _login_to_docker_registries(docker_client: docker.DockerClient) -> Tuple[docker.DockerClient, str]:
    """
    Logs into all docker registries needed to build and deploy the tasks
    :param docker_client:
    :return:
    """
    try:
        docker_client.login(
            username=os.environ["DOCKER_REGISTRY_USERNAME"],
            password=os.environ["DOCKER_REGISTRY_PASSWORD"],
            registry=os.environ["DOCKER_REGISTRY_HOST"]
        )
        ecr_client = get_boto3_client("ecr")
        ecr_registry_token = ecr_client.get_authorization_token()
        ecr_username, ecr_password = base64.b64decode(
            ecr_registry_token["authorizationData"][0]["authorizationToken"]) \
            .decode() \
            .split(":")
        ecr_registry_url = ecr_registry_token["authorizationData"][0]["proxyEndpoint"]
        docker_client.login(
            username=ecr_username,
            password=ecr_password,
            registry=ecr_registry_url
        )
        ecr_repo_base_name = ecr_registry_url.replace('https://', '')
        return docker_client, ecr_repo_base_name
    except DockerException as exception:
        raise TaskBuildError(f"Could not login to docker: {exception}") from exception
