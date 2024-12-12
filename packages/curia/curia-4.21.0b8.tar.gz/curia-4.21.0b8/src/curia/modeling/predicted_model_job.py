import pandas as pd

from curia.api.swagger_client import Dataset
from curia.session import Session
from curia.utils.s3 import load_parquet_files_from_s3


class PredictedModelJob:
    def __init__(self, session: Session, model_job_id: str) -> None:
        self.session = session
        self.model_job_id = model_job_id

    def predictions(self) -> pd.DataFrame:
        """Get the predictions from a model job.

        Returns:
            pd.DataFrame: The predictions.
        """
        predictions_outputs = self.session.api_instance.get_many_base_model_job_output_controller_model_job_output(
            filter=[f"modelJobId||$eq||{self.model_job_id}", "name||$starts||predictions"]
        ).data
        if len(predictions_outputs) == 0:
            raise ValueError(f"No predictions found for model job {self.model_job_id}, verify model job was run"
                             f" successfully and that the job is a prediction job.")
        predictions_output = predictions_outputs[0]

        predictions_dataset: Dataset = self.session.api_instance.get_one_base_dataset_controller_dataset(
            id=predictions_output.dataset_id
        )
        return load_parquet_files_from_s3(predictions_dataset.location)