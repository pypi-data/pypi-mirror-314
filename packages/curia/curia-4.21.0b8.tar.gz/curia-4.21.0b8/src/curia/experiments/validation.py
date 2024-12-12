from typing import (
    Any,
    List,
    Dict,
    Callable,
    Tuple,
)

import mlflow

from curia.experiments.mlflow import MLFlowLogger
from curia.experiments.utils import evaluate_model_on_datasets


def load_mlflow_model(run_id: str) -> Any:
    """
    Load a model from MLFlow using the run_id.

    Parameters:
    run_id (str): The id of the run from which to load the model.

    Returns:
    model: The loaded model.
    """
    try:
        return mlflow.pyfunc.load_model(f"runs:/{run_id}/model")
    except Exception as e:
        raise RuntimeError(f"Could not load model from run {run_id}.") from e


def calculate_metrics(
    run_id: str,
    datasets: Dict[str, Tuple],
    label_col: str,
    prediction_function: Callable,
    metric_func: Callable,
) -> Dict[str, float]:
    """
    Load a model and calculate the validation metrics.

    Parameters:
    run_id (str): The id of the run from which to load the model.
    datasets (Dict[str, Tuple]): The datasets to use for validation.
    label_col (str): The name of the column containing the labels.
    prediction_function (Callable): The function to use to make predictions.
    metric_func (Callable): The function to use to compute the metrics.

    Returns:
    metrics_dict (Dict[str, float]): A dictionary of metric names and their computed values.
    """
    model = load_mlflow_model(run_id)
    try:
        return evaluate_model_on_datasets(
            model=model,
            datasets=datasets,
            label_col=label_col,
            prediction_function=prediction_function,
            metric_func=metric_func,
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to calculate metrics for model from run {run_id}."
        ) from e


def log_metrics(
    run_id: str, metrics_dict: Dict[str, float], tags: Dict[str, str]
) -> None:
    """
    Log the validation metrics to MLFlow.

    Parameters:
    run_id (str): The id of the run from which to load the model.
    metrics_dict (Dict[str, float]): The metrics to log.
    tags (Dict[str, str]): The tags to associate with the logged metrics in MLFlow.
    """

    @MLFlowLogger(run_name=run_id, tags=tags, is_nested=True)
    def log_results() -> Dict[str, float]:
        """
        A decorated function to log the validation results.

        This function is designed to be decorated by MLFlowLogger, which logs
        the results to MLFlow when the function is called.

        Returns:
        metrics_dict (Dict[str, float]): A dictionary of metric names and their computed values.
        """
        return metrics_dict

    log_results()


def track_multiple_experiments(
    run_ids: List[str],
    datasets: Dict[str, Tuple],
    label_col: str,
    tags: Dict[str, str],
    prediction_function: Callable,
    metric_func: Callable,
) -> None:
    """
    Track multiple experiments by logging their validation metrics to MLFlow.

    Parameters:
    run_ids (List[str]): A list of run ids from which to load the models.
    datasets (Dict[str, Tuple]): The datasets to use for validation.
    tags (Dict[str, str]): The tags to associate with the logged metrics in MLFlow.
    metric_func (Callable): The function to use to compute the metrics.
    """
    for run_id in run_ids:
        metrics_dict = calculate_metrics(
            run_id, datasets, label_col, prediction_function, metric_func
        )
        log_metrics(run_id, metrics_dict, tags)
