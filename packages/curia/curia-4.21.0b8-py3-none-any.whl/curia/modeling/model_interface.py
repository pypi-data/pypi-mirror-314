import time
from typing import Union, Literal

from curia.api.swagger_client import Model, ModelJob, ModelJobConfig, ContainerConfig
from curia.modeling.exceptions import InvalidModelError, InvalidModelJobError
from curia.modeling.predicted_model_job import PredictedModelJob
from curia.modeling.trained_model_job import TrainedModelJob
from curia.session import Session


class ModelInterface:
    """
    This class is a wrapper for easier model training. Instantiating the class can be done in two ways:

    1) Using an existing session to create a new model: `ModelInterface.with_new_model(...)`
    2) Using an existing session and model: `ModelInterface(session, model)`

    """

    @classmethod
    def with_new_model(cls,
                       session: Session,
                       experiment_name: str,
                       model_type: str,
                       project_id: str,
                       outcome_type: str
                       ):
        """Instantiate class with an existing session and new model.

        Args:
            session (Session): The session object to use.
            experiment_name (str): The name of the experiment
            model_type (str): The type of model. Can be either "risk" or "impactability".
            project_id (str): The project id for the model.
                Navigate to the folder where you want the model to be built, and copy the part of the url that follows https://aledade.curia.ai/projects/ to get the project_id
            outcome_type (str): Can be either "regression" or "occurrence".

        Returns:
            ModelTrainer: The instantiated class.
        """        """"""
        new_model = cls.create_model(experiment_name, model_type, project_id, outcome_type, session)
        return cls(session, new_model)

    def __init__(self, session: Session, model: Model, model_job_id: str = None):
        """Instantiate the model interface

        Args:
            session (Session): Can be instantiated with the `create_session` static method.
            model (Model): Can be instantiated with the `create_model` static method.
            model_job_id (str, optional): The model job id if the model has already been trained. Defaults to None.
        """
        # Set all parameters
        self.session = session
        self.model = model

        # check model is valid
        self.check_model()

        # Set variables for future use
        self.project_id = self.model.project_id
        self.full_exp_name = self.model.name
        self.outcome_type = self.model.outcome_type

        # model_job_id is set when the model is trained
        self.model_job_id = model_job_id

    @staticmethod
    def create_model(experiment_name: str, model_type: str, project_id: str, outcome_type: str,
                     session: Session) -> Model:
        """Create a new model to be used for training.

        Args:
            experiment_name (str): The name of the experiment.
            model_type (str): The type of model. Can be either "risk" or "impactability".
            project_id (str): The folder where the model will be created. Navigate to the folder where you want the model to be built, and copy the part of the url that follows https://aledade.curia.ai/projects/ to get the project_id
            outcome_type (str): Can be either "regression" or "occurrence".
            session (Session): The session object to use. Can be instantiated with `create_session`.

        Returns:
            Model: The new model.
        """
        # Check outcome_type is valid
        if outcome_type not in ["regression", "occurrence"]:
            raise ValueError("outcome_type must be one of: 'regression', 'occurrence'")

        if model_type not in ["risk", "impactability"]:
            raise ValueError("model_type must be one of: 'risk', 'impactability'")

        # Create a new model object
        new_model = Model(
            name=experiment_name,
            type=model_type,
            feature_store='byod',  # bring your own dataset
            project_id=project_id,
            outcome_type=outcome_type  # can be regression or occurrence
        )
        # Register the new model object
        model = session.api_instance.create_one_base_model_controller_model(new_model)

        return model

    def check_model(self):
        """Validates the model.

        Raises:
            InvalidModelError: The model is invalid.
        """
        try:
            self.session.api_instance.get_one_base_model_controller_model(id=self.model.id)
        except Exception as e:
            raise InvalidModelError(f"Model {self.model.id} is invalid: {e}") from e

    def _create_model_job(self,
                          mode: Union[Literal['train'], Literal['predict']],
                          model_job: ModelJob = None,
                          dataset_id: str = None,
                          config: ModelJobConfig = None) -> ModelJob:
        """Helper that creates a model job from config or from an existing model job object.

        Args:
            model_job (ModelJob, optional): A model job object. Defaults to None.
            dataset_id (str, optional): If no model_job passed, then give dataset id. Defaults to None.
            config (ModelJobConfig, optional): Optional additional parameters for creating the model. Defaults to None.

        Returns:
            ModelJob: The model job object that has been fully created.
        """
        if model_job is None:
            # Instantiate a ModelJob object
            new_model_job = ModelJob(
                model_id=self.model.id,
                dataset_id=dataset_id,
                project_id=self.project_id,
                config=config,
                type=mode,
            )
        else:
            new_model_job = model_job

        # create a model job
        new_model_job_to_run = self.session.api_instance.create_one_base_model_job_controller_model_job(
            new_model_job,
        )

        return new_model_job_to_run

    def _update_model_job(self, new_model_job: ModelJob) -> ModelJob:
        """Helper to update a model job.

        Args:
            new_model_job (ModelJob): The new model job object.

        Returns:
            ModelJob: The updated model job object.
        """
        output_model_job = self.session.api_instance.update_one_base_model_job_controller_model_job(
            id=self.model_job_id,
            body=new_model_job,
        )
        return output_model_job

    def _run_model_job(self, model_job_id: str = None) -> str:
        """Helper function to run a model job.

        Args:`
            model_job_id (str, optional): The model job id. Defaults to None.

        Raises:
            InvalidModelJobError: If the model job does not exist.

        Returns:
            str: The model job id.
        """
        # Set the model_job_id if specified in function
        if model_job_id is not None:
            self.model_job_id = model_job_id
        try:
            self.session.api_instance.model_job_controller_start(
                id=self.model_job_id,
                _preload_content=False,
            )
        except Exception as e:
            if "404" in str(e):
                raise InvalidModelJobError(f"Model job {self.model_job_id} does not exist: {e}") from e
            raise e

    def _wait_for_model_job(self, timeout: int, interval: int, print_status: bool) -> ModelJob:
        """Helper function to wait for a model job to finish.

        Args:
            timeout (int): How long to wait for job to complete in seconds.
            interval (int): How often to check in seconds.
            print_status (bool): Whether to print the status of the model job.

        Raises:
            TimeoutError: If the model job does not finish in the given timeout.

        Returns:
            ModelJob: The model job object.
        """
        if print_status:
            print(f"Printing status of model job every {interval} seconds.")

        start_time = time.time()
        while True:
            if time.time() >= timeout + start_time:
                raise TimeoutError(f"Run operation timed out after {timeout} seconds")
            time.sleep(interval)
            model_job = self.session.api_instance.get_one_base_model_job_controller_model_job(id=self.model_job_id)
            status = model_job.status

            if print_status:
                print(f"Model job status: {status}")

            if status not in ["RUNNING", "STARTING"]:
                return model_job

    def train(self,
              model_job: ModelJob = None,
              dataset_id: str = None,
              model_job_config: ModelJobConfig = None,
              wait: bool = False,
              wait_timeout: int = 3600,
              wait_interval: int = 5,
              print_status: bool = True,
              hyperparameter_default_behavior: str = None,
              hyperparameters: dict = None,
              ) -> TrainedModelJob:
        """The train entrypoint for the model interface.

        Args:
            model_job (ModelJob, optional): If a model job object has already been created. Defaults to None.
            dataset_id (str, optional): If no model_job, this is used to create the model_job object. Defaults to None.
            model_job_config (ModelJobConfig, optional): Optional for additional parameters for the model_job. Defaults to None.
            wait (bool, optional): Whether to wait until finished. Defaults to False.
            wait_timeout (int, optional): If wait, then how long to wait in seconds. Defaults to 3600.
            wait_interval (int, optional): If wait, then how often to checkd. Defaults to 5.
            print_status (bool, optional): Whether to print the status of the model job. Defaults to True.
            hyperparameter_default_behavior (str, optional): The default behavior for hyperparameters. Defaults to None.
            hyperparameters (dict, optional): The hyperparameters to use. Defaults to None.

        Returns:
            TrainedModelJob: the TrainedModelJob object.
        """
        # create the model job
        new_model_job_to_run = self._create_model_job('train', model_job, dataset_id, config=model_job_config)
        self.model_job_id = new_model_job_to_run.id

        # Update the new_model_job_to_run with hyperparameters
        if hyperparameters is not None:
            new_model_job_to_run.config = ModelJobConfig(
                container_config=ContainerConfig(
                    hyperparameter_default_behavior=hyperparameter_default_behavior,
                    hyperparameters=hyperparameters,
                )
            )
            self._update_model_job(new_model_job_to_run)

        # run the model job
        self._run_model_job()

        # wait for the model job to finish
        if wait:
            self._wait_for_model_job(wait_timeout, wait_interval, print_status)

        output = TrainedModelJob(self.session, self.model_job_id)
        return output

    def predict(self,
                model_job: ModelJob = None,
                dataset_id: str = None,
                model_job_config: ModelJobConfig = None,
                wait: bool = False,
                wait_timeout: int = 3600,
                wait_interval: int = 5,
                print_status: bool = True,
                ) -> PredictedModelJob:
        """The predict entrypoint for the model interface.

        Args:
            model_job (ModelJob, optional): If a model job object has already been created. Defaults to None.
            dataset_id (str, optional): If no model_job, this is used to create the model_job object. Defaults to None.
            model_job_config (ModelJobConfig, optional): Optional for additional parameters for the model_job. Defaults to None.
            wait (bool, optional): Whether to wait until finished. Defaults to False.
            wait_timeout (int, optional): If wait, then how long to wait in seconds. Defaults to 3600.
            wait_interval (int, optional): If wait, then how often to checkd. Defaults to 5.
            print_status (bool, optional): Whether to print the status of the model job. Defaults to True.

        Returns:
            PredictedModelJob: the PredictedModelJob object.
        """
        # create the model job
        new_model_job_to_run = self._create_model_job('predict', model_job, dataset_id, config=model_job_config)

        # run the model job
        self.model_job_id = new_model_job_to_run.id
        self._run_model_job()

        # wait for the model job to finish
        if wait:
            self._wait_for_model_job(wait_timeout, wait_interval, print_status)

        return PredictedModelJob(self.session, self.model_job_id)
