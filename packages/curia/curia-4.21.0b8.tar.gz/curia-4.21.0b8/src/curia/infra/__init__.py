try:
    import docker
    import pyspark
except ImportError as exc:
    raise ImportError(
        "Some optional dependencies required for curia.infra are missing. "
        "Please install them via `poetry install --with=infra` if developing or"
        " `pip install curia[infra]` if using curia as a library."
    ) from exc
