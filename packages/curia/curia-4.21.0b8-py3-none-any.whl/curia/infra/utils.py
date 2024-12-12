import importlib
import inspect
import os
import pkgutil
import sys
import typing

import click

from curia.infra.task import TaskDefinition


T = typing.TypeVar('T', bound=TaskDefinition)


class AdditionalPath:
    """
    Context manager for adding a path to sys.path. Removes the path when the context exits.
    Useful for when you want to import a module from a path that isn't in sys.path and you don't want to pollute
    sys.path with the new path for the rest of the process (for example, during testing).
    """
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass


class ContextualImportManager:
    """
    Context manager for importing modules that you later don't want to be able to import.
    Useful for when you want to import a module from a path that isn't in sys.path and you don't want that module to
    be available for the rest of the process (for example, during testing).
    """
    def __init__(self):
        self.imported_modules = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for module_name in self.imported_modules:
            del sys.modules[module_name]

    def import_module(self, module_name):
        module = importlib.import_module(module_name)
        self.imported_modules.append(module_name)
        return module


def load_tasks(project_dir: str, package: str, task_type: typing.Type[T]) -> typing.List[T]:
    """
    Loads all tasks in package by importing every module

    :param project_dir: The project directory to load tasks from
    :param package: The package to load tasks from
    :param task_type: The type of task to load
    :return:
    """
    with AdditionalPath(os.path.join(project_dir, "src")), ContextualImportManager() as contextual_import_manager:
        # pylint: disable=import-outside-toplevel
        # recursively import all tasks
        root_package = contextual_import_manager.import_module(package)
        registry = TaskDefinition.Registry()
        for _, module_name, _ in pkgutil.walk_packages(
                path=root_package.__path__, prefix=root_package.__name__ + "."
        ):
            click.echo(f"Searching for tasks in {module_name}")
            module = contextual_import_manager.import_module(module_name)
            for _, obj in inspect.getmembers(module):
                if isinstance(obj, task_type) and obj != TaskDefinition:
                    registry.register(obj)
                elif isinstance(obj, TaskDefinition):
                    click.echo(f"Found task {obj.task_slug} of incorrect type {type(obj)}, skipping")

    return registry.list()


def describe_tasks(tasks: typing.List[TaskDefinition], verbose=False) -> None:
    """
    Describes all listed tasks
    :param tasks: List of tasks to describe
    :param verbose: If true, will print out the full description of each task
    :return:
    """
    task_descriptions = []
    short_task_list = []
    for task in tasks:
        task_descriptions.append("--------------------")
        task_descriptions.extend(task.describe())
        task_descriptions.append("--------------------")
        task_descriptions.append("")
        short_task_list.append(f"{task.task_slug}")
    task_names_and_descrs = "\n".join(task_descriptions)
    short_task_list_str = "\n".join([f"    {t}" for t in short_task_list])
    if not verbose:
        click.echo(short_task_list_str)
    else:
        click.echo(f"""
Found tasks:
{task_names_and_descrs}

Short task list:
{short_task_list_str}

{len(tasks)} tasks found
        """)
