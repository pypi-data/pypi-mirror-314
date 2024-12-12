try:
    import docker
except ImportError as exc:
    raise ImportError(
        "Some optional dependencies required for curia.infra.container are missing. "
        "Please install them via `poetry install --with=container_infra` if developing or"
        " `pip install curia[container_infra]` if using curia as a library."
    ) from exc
