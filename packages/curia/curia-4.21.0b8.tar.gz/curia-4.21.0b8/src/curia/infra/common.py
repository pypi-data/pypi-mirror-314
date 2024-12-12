import os
import typing

import click

from curia.api.swagger_client import Workflow, WorkflowTemplate, Task
from curia.infra.task import TaskDefinition
from curia.infra.types import TaskDeployResourceNamingConfig, TaskType
from curia.session import Session


def update_curia_task_and_stub_workflow(task: TaskDefinition,
                                        stage: str,
                                        resource_naming_config: TaskDeployResourceNamingConfig,
                                        task_specific_context: dict) -> None:
    """
    Creates or updates the curia task definition for a task in the curia platform using the curia SDK
    :param task: The task definition
    :param stage: The stage to deploy the task to
    :param resource_naming_config: The resource naming config to use when creating the task
    :param task_specific_context: The task specific context to use when creating the task, identifying external
    resources specific to the task like databricks job IDs or ECS task definitions
    :return:
    """
    session = Session(
        api_token=os.environ["CURIA_API_KEY"],
        host=os.environ["CURIA_API_ENDPOINT"]
    )

    internal_task_name = f"{resource_naming_config.platform_task_prefix}{stage}-{task.task_slug}"

    task_id = _create_or_update_task(
        session=session,
        task=task,
        internal_task_name=internal_task_name,
        task_type=task.task_type,
        task_specific_context=task_specific_context
    )

    workflow_template_id = _create_or_update_workflow_template(
        session,
        stage,
        task,
        task_id,
        resource_naming_config,
        task_specific_context
    )

    workflow_id = _create_or_update_workflow(session, task, internal_task_name, workflow_template_id)

    click.echo(f"""
Created or updated workflow ecosystem {internal_task_name} with data:
workflow_id: {workflow_id}
workflow_template_id: {workflow_template_id}
task_id: {task_id}
    """)


def _create_or_update_workflow(
        session: Session,
        task: TaskDefinition,
        task_name: str,
        workflow_template_id: str) -> str:
    """
    Creates or updates a workflow in the curia platform
    :param session: curia session
    :param task: task definition that is managing the workflow
    :param task_name: name of the workflow
    :param workflow_template_id: id of the workflow template to use with this workflow
    :return:
    """
    # get the workflow, if it exists
    results = session.api_instance.get_many_base_workflow_controller_workflow(
        filter=[f"name||$eq||{task_name}"]
    )
    if len(results.data) == 0:
        # create the workflow
        workflow_id = typing.cast(str, session.api_instance.create_one_base_workflow_controller_workflow(
            Workflow(
                name=task_name,
                description=task.description,
                organization_id=os.environ["CURIA_PRIMARY_ORGANIZATION_ID"],
                template_id=workflow_template_id
            )
        ).id)
    elif len(results.data) == 1:
        existing_workflow = results.data[0]
        workflow_id = typing.cast(str, existing_workflow.id)
        # update the workflow
        existing_workflow.template_id = workflow_template_id
        existing_workflow.name = task_name
        existing_workflow.description = task.description
        session.api_instance.update_one_base_workflow_controller_workflow(
            id=workflow_id,
            body=existing_workflow
        )
    else:
        raise ValueError(f"Found multiple workflows with name {task_name}. This should not "
                         f"happen, please clean up the present workflows in the curia platform")
    return workflow_id


def _create_or_update_workflow_template(
        session: Session,
        env: str,
        task: TaskDefinition,
        task_id: str,
        resource_naming_config: TaskDeployResourceNamingConfig,
        task_specific_context: dict) -> str:
    """
    Creates or updates a workflow template in the curia platform
    :param session: curia session
    :param env: environment to use (dev, stage, prod)
    :param task: task definition that is managing the workflow template
    :param task_id: id of the task to use with this workflow template
    :param resource_naming_config: resource naming config
    :param task_specific_context: task specific context
    :return:
    """
    new_workflow_template = WorkflowTemplate(
        name=f"{resource_naming_config.platform_workflow_prefix}{env}-{task.task_slug}",
        description=task.description,
        parameters={
            **{
                task_input.name: "" for task_input in task.inputs
            }
        },
        definition={
            "taskId": task_id,
            "data": {
                **task.build_workflow_data_block(task.inputs, task_specific_context)
            },
            "opts": {},
            "children": []
        },
        organization_id=os.environ["CURIA_PRIMARY_ORGANIZATION_ID"]
    )
    # get the workflow template, if it exists
    results = session.api_instance.get_many_base_workflow_template_controller_workflow_template(
        filter=[f"name||$eq||{new_workflow_template.name}"]
    ).data
    if len(results) == 0:
        # create the workflow template
        workflow_template_id = typing.cast(str, session.api_instance
                                           .create_one_base_workflow_template_controller_workflow_template(
            new_workflow_template).id)
    elif len(results) == 1:
        workflow_template_id = typing.cast(str, results[0].id)
        # update the workflow template
        session.api_instance.update_one_base_workflow_template_controller_workflow_template(
            id=workflow_template_id,
            body=new_workflow_template
        )
    else:
        raise ValueError(f"Found multiple workflow templates with name {new_workflow_template.name}. This should not "
                         f"happen, please clean up the present workflow templates in the curia platform")
    return workflow_template_id


def _create_or_update_task(
        session: Session,
        task: TaskDefinition,
        internal_task_name: str,
        task_type: TaskType,
        task_specific_context: dict) -> str:
    """
    Creates or updates a task in the curia platform using the curia SDK
    :param session: curia session
    :param task: task definition that is managing the task's deployment
    :param internal_task_name: name of the task
    :param task_type: type of the task
    :param task_specific_context: task specific context
    :return:
    """
    new_task = Task(
        name=internal_task_name,
        description=task.description,
        type=task_type.value,
        inputs=task.build_task_inputs(task.inputs, task_specific_context),
        outputs={
            task_output.name: {
                "descr": task_output.description
            } for task_output in task.outputs
        },
        organization_id=os.environ["CURIA_PRIMARY_ORGANIZATION_ID"],
    )
    # get the task definition, if it exists
    results = session.api_instance.get_many_base_task_controller_task(
        filter=[f"name||$eq||{internal_task_name}"]
    ).data
    if len(results) == 0:
        # create the task definition
        task_id = typing.cast(str, session.api_instance.create_one_base_task_controller_task(new_task).id)
    elif len(results) == 1:
        # update the task definition
        task_id = typing.cast(str, results[0].id)

        session.api_instance.update_one_base_task_controller_task(
            id=task_id,
            body=new_task
        )
    else:
        raise ValueError(
            f"Found multiple tasks with name {internal_task_name}. This should not happen, please clean up the "
            f"present tasks in the curia platform")
    return task_id
