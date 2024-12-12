import functools
from typing import Any, Callable, Dict

from hyperopt import fmin, tpe, STATUS_OK
from hyperopt.spark import SparkTrials


class HyperoptTuner:
    """
    A class for hyperparameter tuning using hyperopt.

    Attributes:
        search_space: A dictionary representing the search space.
        max_evals: The maximum number of evaluations.
        spark_trials: An instance of SparkTrials to distribute the tuning across a Spark cluster.

    Methods:
        __call__: A method that makes the class instance callable. It wraps the passed function and
        optimizes the function's parameters according to the search space.
    """

    def __init__(
        self,
        search_space: Dict[str, Any],
        max_evals: int,
        spark_trials: SparkTrials = None,
    ) -> None:
        """
        The constructor for the HyperoptTuning class.
        """
        self.search_space = search_space
        self.max_evals = max_evals
        self.spark_trials = spark_trials

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Makes the class instance callable.
        """

        @functools.wraps(func)
        def wrapped_func(**kwargs: Any) -> Dict[str, Any]:
            """
            The wrapped function that will run the optimization process.
            """

            def objective(params: Dict[str, Any]) -> Dict[str, Any]:
                """
                The objective function to be minimized.
                """
                return {
                    "loss": func(params, **kwargs),
                    "status": STATUS_OK,
                }

            best_params = fmin(
                objective,
                self.search_space,
                algo=tpe.suggest,
                max_evals=self.max_evals,
                trials=self.spark_trials,
            )
            return best_params

        return wrapped_func


def using_hyperopt_tuning(
    search_space: Dict[str, Any], max_evals: int, spark_trials: SparkTrials = None
) -> Callable:
    """
    A convenience function for using the HyperoptTuner class as a decorator.

    Args:
        search_space (Dict[str, Any]): A dictionary representing the search space.
        max_evals (int): The maximum number of evaluations.
        spark_trials (SparkTrials, optional): An instance of SparkTrials to distribute the tuning across a Spark cluster
        Defaults to None.

    Returns:
        Callable: A decorator for tuning hyperparameters using hyperopt.
    """
    tuner = HyperoptTuner(search_space, max_evals, spark_trials)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return tuner(func)

    return decorator
