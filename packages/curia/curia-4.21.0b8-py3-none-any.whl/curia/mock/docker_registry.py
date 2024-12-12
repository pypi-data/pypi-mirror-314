import functools
import os
import secrets
import subprocess
import time
from pathlib import Path
from typing import Callable, Any, Optional


TEMP_DOCKER_REGISTRY_SUBFOLDER = "docker_registry"

DOCKER_REGISTRY_VERSION = "2.8.2"


def _generate_random_password():
    """
    Generates a random password for the docker container. NOT SECURE.
    """
    return secrets.token_urlsafe(20)


def _setup_local_docker_registry_credentials(
        mock_registry_folder: Path,
        username: str = 'local_test',
        password: Optional[str] = None):
    """
    Sets up the local docker registry credentials.
    :param mock_registry_folder: The temp folder to use for the mock registry.
    :param username: The username to use for the local docker registry.
    :param password: The password to use for the local docker registry. If None, a random password will be generated.
    """
    # create the auth directory
    auth_folder = mock_registry_folder / "auth"
    auth_folder.mkdir(parents=True, exist_ok=True)
    # generate the password if necessary
    if password is None:
        password = _generate_random_password()
    # docker run --entrypoint htpasswd registry:2 -Bbn local_test password > auth/htpasswd
    try:
        result = subprocess.run(
            [
                "docker",
                "run",
                "--entrypoint",
                "htpasswd",
                "httpd:2",
                "-Bbn",
                username,
                password
            ],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to generate htpasswd file: {e}\n{e.stderr}") from e
    # write the password to the file
    with open(auth_folder / "htpasswd", "w", encoding="utf-8") as f:
        f.write(result.stdout.decode("utf-8"))
    return username, password, auth_folder


def setup_local_docker_registry(
        port: int = 3001,
        temp_folder: Path = Path("./temp/"),
        username: str = 'local_test',
        password: Optional[str] = None
):
    """
    Sets up a local docker registry for testing purposes running on the given port.
    :param port: The port to run the registry on.
    :param temp_folder: The temp folder to use for the mock registry.
    :param username: The username to use for the local docker registry.
    :param password: The password to use for the local docker registry. If None, a random password will be generated.

    :return: tuple of the container id and a dictionary containing the username, password, and host that the docker
    registry is running on.
    """
    mock_registry_folder = temp_folder / TEMP_DOCKER_REGISTRY_SUBFOLDER
    # create the mock registry folder
    mock_registry_folder.mkdir(parents=True, exist_ok=True)
    username, password, auth_folder = _setup_local_docker_registry_credentials(
        mock_registry_folder=mock_registry_folder,
        username=username,
        password=password
    )
    try:
        process = subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "-p",
                f"{port}:5000",
                "--name",
                "mock-registry",
                "-v",
                f"{auth_folder.resolve()}:/auth",
                "-e",
                "REGISTRY_AUTH=htpasswd",
                "-e",
                "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm",
                "-e",
                "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd",
                f"registry:{DOCKER_REGISTRY_VERSION}"
            ],
            capture_output=True,
            check=True
        )
        # wait a second for the container to start
        time.sleep(1)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to start docker registry: {e}\n{e.stderr}") from e
    # get the container id from the process
    container_id = process.stdout.decode("utf-8").strip()
    return container_id, {
        "username": username,
        "password": password,
        "host": f"localhost:{port}"
    }


def teardown_local_docker_registry(
        container_id: str,
        temp_folder: Path = Path("./temp/")
):
    """
    Tears down the local docker registry running on the given port and deletes the relevant temp files.
    """
    registry_folder = temp_folder / TEMP_DOCKER_REGISTRY_SUBFOLDER

    #  docker stop mock-registry
    try:
        subprocess.run(
            [
                "docker",
                "stop",
                container_id
            ],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to stop docker registry: {e}\n{e.stderr}") from e
    # docker rm mock-registry
    try:
        subprocess.run(
            [
                "docker",
                "rm",
                container_id
            ],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to remove docker registry: {e}\n{e.stderr}") from e
    # rm -rf registry
    os.system(f"rm -rf {registry_folder}")


def using_local_docker_registry(port: int = 3001,
                                temp_folder: Path = Path("./temp/"),
                                username: str = 'local_test',
                                password: Optional[str] = None):
    """
    Decorator for tests that require a local docker registry. Automatically sets up the registry, runs the wrapped
    function, and tears down the registry.

    :param port: The port to run the registry on.
    :param temp_folder: The temp folder to use for the mock registry.
    :param username: The username to use for the local docker registry.
    :param password: The password to use for the local docker registry. If None, a random password will be generated.
    """
    def decorator(fn) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            registry_id, credentials = setup_local_docker_registry(
                port=port,
                temp_folder=temp_folder,
                username=username,
                password=password
            )
            try:
                return fn(*args, **kwargs, docker_registry_credentials=credentials)
            finally:
                teardown_local_docker_registry(
                    registry_id,
                    temp_folder=temp_folder
                )

        return wrapper
    return decorator
