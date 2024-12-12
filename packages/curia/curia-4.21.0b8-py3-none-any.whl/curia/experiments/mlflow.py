import functools
from typing import Callable, Dict, Any, Union
from curia.experiments.utils import MLFLowDatabricksCredentials
import mlflow
import os
import pandas as pd

class MLFlowLogger:
    def __init__(self,
                 run_name: str = None,
                 tags: Dict[str, Any] = None,
                 autolog: bool = False,
                 is_nested: bool = False,
                 mlflow_databricks_credentials: MLFLowDatabricksCredentials = None) -> None:
        """
        Refer to using_mlflow_logging for documentation.
        """
        self.run_name = run_name
        self.tags = tags
        self.autolog = autolog
        self.is_nested = is_nested
        if mlflow_databricks_credentials is not None:
            self._set_env_variables(mlflow_databricks_credentials)

    def _set_env_variables(self, mlflow_databricks_credentials: MLFLowDatabricksCredentials) -> None:
        """Helper function for setting environment variables for logging to Databricks.

        Args:
            mlflow_databricks_credentials (MLFLowDatabricksCredentials): The credentials for logging to Databricks.
        """
        os.environ['MLFLOW_TRACKING_URI'] = "databricks"
        os.environ['DATABRICKS_HOST'] = mlflow_databricks_credentials.host
        os.environ['DATABRICKS_TOKEN'] = mlflow_databricks_credentials.token
        mlflow.set_experiment(mlflow_databricks_credentials.experiment_name)

    @staticmethod
    def log_items(items_to_log: Dict[str, Union[float, pd.DataFrame, int, str]]):
        """Called by the decorator to log items to MLFlow.

        Args:
            items_to_log (Dict[str, Union[float, pd.DataFrame]]): A dictionary of items to log to MLFlow.
        """
        if not isinstance(items_to_log, dict):
            raise TypeError("items_to_log must be a dictionary")
        for metric_name, metric_value in items_to_log.items():
            if isinstance(metric_value, pd.DataFrame):
                if ".json" not in metric_name:
                    metric_name += ".json"
                mlflow.log_table(artifact_file=metric_name, data=metric_value)
            else:
                mlflow.log_metric(metric_name, metric_value)

    @staticmethod
    def log_params(params: Dict[str, Any]):
        """Called by the decorator to log parameters to MLFlow.

        Args:
            params (Dict[str, Any]): A dictionary of parameters to log to MLFlow.
        """
        if not isinstance(params, dict):
            raise TypeError("params must be a dictionary")
        mlflow.log_params(params)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.autolog:
                mlflow.autolog(log_datasets=False, log_models=True)
            with mlflow.start_run(
                nested=self.is_nested, run_name=self.run_name, tags=self.tags
            ):
                result = func(*args, **kwargs)

                # If the function returns a dictionary, log it.
                if isinstance(result, dict):
                    self.log_items(result)

            return result

        return wrapper


def using_mlflow_logging(
    run_name: str = None,
    tags: Dict[str, Any] = None,
    autolog: bool = False,
    is_nested: bool = False,
    mlflow_databricks_credentials: MLFLowDatabricksCredentials = None,
) -> Callable:
    """
    A convenience function for using the MLFlowLogger class as a decorator.

    Args:
        run_name (str, optional): The name of the run. Defaults to None.
        tags (Dict[str, Any], optional): A dictionary of tags to add to the run. Defaults to None.
        autolog (bool, optional): Whether to use MLFlow's autologging feature. Defaults to False.
        is_nested (bool, optional): Whether the run is nested within another run. Defaults to False.
        mlflow_databricks_credentials (MLFLowDatabricksCredentials, optional): Credentials for logging to Databricks. Defaults to None.

    Returns:
        Callable: A decorator for logging MLFlow runs.
    """

    logger = MLFlowLogger(run_name, tags, autolog, is_nested, mlflow_databricks_credentials)

    def decorator(func: Callable) -> Callable:
        return logger(func)

    return decorator
