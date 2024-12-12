from curia.session import Session
import pandas as pd
import numpy as np
from typing import Dict, List, Callable

from curia.api.swagger_client.models.model_job_output_response_dto import ModelJobOutputResponseDto

class MetricsInterface:
    metric_factories = dict()
    """
    A class to simplify the model job output extraction process.

    Much of this code was originally in:
    https://dbc-5c784d6d-d7a7.cloud.databricks.com/?o=1189584077923919#notebook/3744383587579554/command/3744383587579629
    """

    @classmethod
    def _get_raw_outputs(cls, session: Session, model_job_id: str) -> List[ModelJobOutputResponseDto]:
        """Query the API for all outputs of a model job.

        Args:
            session (Session): The session object to use.
            model_job_id (str): The model job from which to get the outputs.

        Returns:
            List[ModelJobOutputResponseDto]: The full list of outputs from the model job.
        """
        raw_outputs = session.api_instance.get_many_base_model_job_output_controller_model_job_output(
            filter=[f"modelJobId||$eq||{model_job_id}"]  # gt, lt, neq
        ).data
        return raw_outputs

    @classmethod
    def _get_named_output_with_session(cls,
                          session: Session,
                          output_name: str,
                          model_job_id: str,
                          ) -> ModelJobOutputResponseDto:
        # fetch raw outputs if not provided

        raw_outputs = cls._get_raw_outputs(session, model_job_id)
        # get named output
        return cls._get_named_output(raw_outputs, output_name)

    @classmethod
    def get_named_output_with_session(cls,
                          session: Session,
                          output_name: str,
                          model_job_id: str,
                          ) -> ModelJobOutputResponseDto:
        """Fetch a named output from a model job output.

        Args:
            session (Session): The session object to use.
            output_name (str): The name of the output to fetch.
            model_job_id (str): The model job from which to get the output.

        Returns:
            ModelJobOutputResponseDto: The named output.
        """
        return cls._get_named_output_with_session(session, output_name, model_job_id)

    @classmethod
    def _get_named_output(cls, raw_outputs: List[ModelJobOutputResponseDto], output_name: str) -> ModelJobOutputResponseDto:
        try:
            named_output = [output for output in raw_outputs if output.name == output_name][0]
        except IndexError as e:
            raise ValueError(f"No output with name {output_name} found.") from e

        return named_output


    @classmethod
    def get_basic_metrics(cls, session: Session, model_job_id: str) -> Dict[str, float or int]:
        """Extracting the most basic metrics from the model job as a dictionary.

        Args:
            session (Session): The session object to use.
            model_job_id (str): The model job id from which to get the metrics

        Returns:
            Dict[str, float or int]: _description_
        """
        model_summary = cls._get_named_output_with_session(session, "model-summary", model_job_id)
        metrics = model_summary.data["metrics"]
        return metrics

    @classmethod
    def get_registered_metrics(cls) -> List[str]:
        """Get the names of metrics that can be used with the get_metrics function.

        Returns:
            List[str]: The list of metric names.
        """
        return list(cls.metric_factories.keys())

    @classmethod
    def _remove_na(cls, dirty_output: pd.DataFrame, replacement: int = 0):
        """Helper function to remove NA and np.nan from a dictionary.

        Args:
            dirty_output (pd.DataFrame): The dataframe with dirty values.
            replacement (int, optional): What value to put in the cleaned dictionary. Defaults to 0.

        """
        to_replace = [None, np.nan, "NA"]
        dirty_output.replace(to_replace, replacement, inplace=True)

    @classmethod
    def get_metrics(cls,
                    session: Session,
                    metric_names: List[str],
                    model_job_id: str) -> Dict[str, float or int]:
        """Get the metrics named in 'metric_names' from the model job.

        Args:
            session (Session): The session object to use.
            metric_names (List[str]): The metrics to pull.
            model_job_id (str): The model job from which to get output.

        Raises:
            ValueError: If any metric is not a registered metric

        Returns:
            Dict[str, float or int]: The metrics requested.
        """
        raw_outputs = cls._get_raw_outputs(session, model_job_id)
        # Check that all metrics are registered
        registered_metric_names = cls.get_registered_metrics()
        for metric in metric_names:
            if metric not in registered_metric_names:
                raise ValueError(f"Metric {metric} is not registered. Registered metrics are: {registered_metric_names}")

        # calculate the metrics and add them to the output
        output = dict()
        for metric_name in metric_names:
            output[metric_name] = cls.metric_factories[metric_name](raw_outputs)

        return output

def register_metric(metric_name: str):
    """Register a metric with the instance.

    Args:
        metric_name (str): The name of the metric.
    """
    def decorator(concrete_method: Callable[[List[ModelJobOutputResponseDto]], float or pd.DataFrame or bool or int]):
        MetricsInterface.metric_factories[metric_name] = concrete_method
        return concrete_method
    return decorator


@register_metric("auc")
def _get_auc(raw_outputs: List[ModelJobOutputResponseDto]) -> float:
    """
    Get the auc_roc from the model outputs for 'occurrence' models.
    """
    model_summary = MetricsInterface._get_named_output(raw_outputs, "model-summary")
    output = model_summary.data["metrics"]["auc_roc"]
    return output

@register_metric("r2")
def _get_r2(raw_outputs: List[ModelJobOutputResponseDto]) -> float:
    """
    Get the r2 from the model outputs for 'regression' models.
    """
    model_summary = MetricsInterface._get_named_output(raw_outputs, "model-summary")
    output = model_summary.data["metrics"]["r2"]
    return output

@register_metric("smd")
def _get_smd(raw_outputs: List[ModelJobOutputResponseDto]) -> pd.DataFrame:
    """
    Get the smd from model outputs.
    """
    smd_features = MetricsInterface._get_named_output(raw_outputs, "top-features")
    output = smd_features.data
    output_df = pd.DataFrame(output)
    MetricsInterface._remove_na(output_df)
    return output_df

@register_metric("shap")
def _get_shap(raw_outputs: List[ModelJobOutputResponseDto]) -> pd.DataFrame:
    """
    Gets shap values from model outputs.
    """
    shap_features = MetricsInterface._get_named_output(raw_outputs, "shap-features")
    output = shap_features.data
    output_df = pd.DataFrame(output)
    # Transpose and rename index -> feature for consistency with smd
    output_df = output_df.T.reset_index()
    output_df.rename(columns={"index": "feature"}, inplace=True)
    MetricsInterface._remove_na(output_df)
    return output_df

@register_metric("decile_gain")
def _get_decile_gain(raw_outputs: List[ModelJobOutputResponseDto]) -> pd.DataFrame:
    """
    Get the decile gain from model outputs.
    """
    decile_gain = MetricsInterface._get_named_output(raw_outputs, "bin-summary")
    output = decile_gain.data
    output_df = pd.DataFrame(output)
    MetricsInterface._remove_na(output_df)
    return output_df
