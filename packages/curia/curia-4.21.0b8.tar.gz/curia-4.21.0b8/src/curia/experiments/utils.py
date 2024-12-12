from typing import Dict, Any, Callable

import mlflow
from dataclasses import dataclass

@dataclass
class MLFLowDatabricksCredentials:
    """ A class for storing Databricks credentials.

    Parameters:
        email: The email address of the user.
        host: The host of the Databricks workspace.
        token: The Databricks token.
        experiment_name: The name of the MLFlow experiment.

    """
    email: str
    host: str
    token: str
    experiment_name: str

    def __post_init__(self) -> None:
        self._validate_email()
        self.validate_experiment_name()

    def _validate_email(self) -> None:
        if "@" not in self.email:
            raise ValueError("Invalid email address, must contain '@'")

    def validate_experiment_name(self) -> None:
        if not self.experiment_name.startswith(("/Users", "/Shared")):
            possible_experiment_name = f"/Users/{self.email}/{self.experiment_name}"
            raise ValueError(f"Invalid experiment name, consider using '{possible_experiment_name}'")


def make_predictions(model: Any, data: Any, prediction_function: Callable) -> Any:
    """
    Makes predictions using the provided model and data.

    Parameters:
        model: The model to be used.
        data: The data on which to make predictions.
        prediction_function: The function to use for making predictions. This function should take a model and a dataset
        as inputs and return predictions.

    Returns:
        The predictions made by the model on the data.

    Example:
        The `prediction_function` could be a function like the following:
        def predict(model, data):
            return model.predict(data)

    """
    return prediction_function(model, data)


def evaluate_predictions(
    y_true: Any, y_pred: Any, metric_func: Callable
) -> Dict[str, float]:
    """
    Evaluates predictions using the provided metric function.

    Parameters:
        y_true: The true target values.
        y_pred: The predicted target values.
        metric_func: The function used to compute the metrics. This function should take true and predicted values as
        inputs and return a dictionary mapping metric names to computed metric values.

    Returns:
        A dictionary mapping metric names to computed metric values.
        Example: {'log_loss': 0.123, 'roc_auc': 0.456}

    Example:
        The `metric_func` could be a function like the following:

        def compute_metrics(y_true, y_pred):
            precision = metrics.precision_score(y_true, y_pred)
            recall = metrics.recall_score(y_true, y_pred)

            return {"precision": precision, "recall": recall}
    """
    return metric_func(y_true, y_pred)


def evaluate_model_on_datasets(
    model: Any,
    datasets: Dict[str, Any],
    prediction_function: Callable,
    metric_func: Callable,
    label_col: str = "label",
) -> Dict[str, float]:
    """
    Evaluates a model's performance across multiple datasets using a specified metric function.

    Parameters:
        model: The model to be evaluated.
        datasets: A dictionary mapping dataset names to datasets.
        prediction_function: The function to use for making predictions. This function should take a model and a dataset
        as inputs and return predictions.
        metric_func: The function used to compute the metrics. This function should take true and predicted values as
        inputs and return a dictionary mapping metric names to computed metric values.
        label_col: The name of the column containing the true target values.

    Returns:
        A dictionary mapping "{dataset_name}_{metric_name}" to computed metric values.
    """

    results = {}

    for name, data in datasets.items():
        # Make predictions
        y_true = data[label_col]
        y_pred = make_predictions(
            model, data.drop(columns=[label_col]), prediction_function
        )

        # Compute metrics
        metrics = evaluate_predictions(y_true, y_pred, metric_func)

        # Store results in dictionary
        for metric_name, metric_value in metrics.items():
            results[f"{name}_{metric_name}"] = metric_value

    return results


def get_mlflow_run(id_value, id_type="runName"):
    """
    Retrieve the MLFlow run with the specified ID value and type.

    :param id_value: The value of the ID to search for.
    :param id_type: The type of the ID to search for.
    to 'runName'.
    :return: The MLFlow run with the specified ID value and type.
    """
    assert id_type in ["runName", "parentRunId"], "Invalid ID type"

    # Use mlflow.search_runs to find the run by its ID
    runs = mlflow.search_runs(filter_string=f"tags.mlflow.{id_type}='{id_value}'")
    assert len(runs) == 1, "The number of runs with the specified ID is not exactly 1"

    # Return the first (and only) run
    return runs.iloc[0]
