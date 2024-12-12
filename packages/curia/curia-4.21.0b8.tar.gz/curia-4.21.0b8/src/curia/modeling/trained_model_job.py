from curia.modeling.metrics import MetricsInterface
from curia.session import Session

from curia.api.swagger_client.models.model_job_output_response_dto import ModelJobOutputResponseDto

from typing import Dict, List
import pandas as pd

class TrainedModelJob:
    def __init__(self, session: Session, model_job_id: str) -> None:
        self.session = session
        self.model_job_id = model_job_id

    def get_basic_metrics(self) -> Dict[str, float]:
        """Extract basic metrics from a model job.

        Returns:
            Dict[str, float]: A dictionary of the metrics.
        """
        basic_metrics = MetricsInterface.get_basic_metrics(self.session, self.model_job_id)
        return basic_metrics

    def all_named_metrics(self) -> List[str]:
        """Get the possible named metrics

        Returns:
            List[str]: The list of named metrics.
        """
        metric_names = MetricsInterface.get_registered_metrics()
        return metric_names

    def get_metrics(self, metrics_to_get: List[str]) -> Dict[str, float or pd.DataFrame]:
        """Gets a set of metrics listed in 'metrics' from the model trained or model_job_id.

        Args:
            metrics_to_get (List[str]): The list of metrics to get. A full list can be found with the `all_named_metrics` method.

        Returns:
            Dict[str, float or pd.DataFrame]: A dictionary of the metrics.
        """
        output_metrics_dict = MetricsInterface.get_metrics(self.session, metrics_to_get, self.model_job_id)
        return output_metrics_dict

    def get_metric_from_outputs(self, metric_title: str) -> ModelJobOutputResponseDto:
        """Gets a metric from the model's raw outputs.

        Args:
            metric_title (str): The name of the metric to get.

        Returns:
            Any: The metric.
        """
        output_metric = MetricsInterface.get_named_output_with_session(self.session, metric_title, self.model_job_id)
        return output_metric
