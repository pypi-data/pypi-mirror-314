try:
    import pyspark
except ImportError as exc:
    raise ImportError(
        "Some optional dependencies required for curia.infra.databricks are missing. "
        "Please install them via `poetry install --with=databricks_infra` if developing or"
        " `pip install curia[databricks_infra]` if using curia as a library."
    ) from exc
