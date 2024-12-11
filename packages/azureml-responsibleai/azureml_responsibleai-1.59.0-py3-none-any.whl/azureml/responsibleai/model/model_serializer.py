# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""ModelSerializer class to save and load AzureML models."""

import logging

from typing import Any
from azureml.core import Model, Run, Workspace

try:
    import mlflow
    mlflow_import_error = False
except ImportError:
    mlflow_import_error = True


_logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def log_info(message):
    """Log info message.

    :param message: Message to log.
    :type message: str
    """
    _logger.info(message)
    print(message)


class ModelSerializer:
    """Class to save and load AzureML models."""

    def __init__(self, model_id: str, workspace: Workspace,
                 model_type: str = "pyfunc"):
        """Initialize ModelSerializer.

        :param model_id: Model ID.
        :type model_id: str
        :param workspace: Workspace.
        :type workspace: Workspace
        :param model_type: Model type, defaults to "pyfunc"
        :type model_type: str, optional
        """
        self._model_id = model_id
        self._model_type = model_type
        self._subscription_id = workspace.subscription_id
        self._resource_group = workspace.resource_group
        self._workspace_name = workspace.name

    def save(self, model, path):
        """Save the AzureML model.

        The method does nothing since the model is already saved in AzureML.

        :param model: Model to save.
        :type model: Any
        :param path: Path to save the model.
        :type path: str
        """
        # Nothing to do, since model is saved in AzureML
        pass

    def load(self, path):
        """Load the AzureML model.

        :param path: Path to load the model.
        :type path: str
        :return: Loaded model.
        :rtype: Any
        """
        return self.load_mlflow_model(self._model_id)

    def load_mlflow_model(self, model_id: str) -> Any:
        """Load the AzureML model using MLflow.

        :param model_id: Model ID.
        :type model_id: str
        :return: Loaded model.
        :rtype: Any
        """
        try:
            my_run = Run.get_context()
            workspace = my_run.experiment.workspace
        except Exception as e:
            log_info("Failed to get workspace from Run context")
            log_info(e)
            log_info("Try to setup workspace from saved state")
            workspace = Workspace(subscription_id=self._subscription_id,
                                  resource_group=self._resource_group,
                                  workspace_name=self._workspace_name)

        if mlflow_import_error:
            error = "mlflow not installed, cannot use ModelSerializer"
            raise ImportError(error)

        mlflow.set_tracking_uri(workspace.get_mlflow_tracking_uri())

        model = Model._get(workspace, id=model_id)
        model_uri = "models:/{}/{}".format(model.name, model.version)
        if self._model_type == "fastai":
            fastai_model = mlflow.fastai.load_model(model_uri)
            log_info("fastai_model: {0}".format(type(fastai_model)))
            log_info(f"dir(fastai_model): {dir(fastai_model)}")
            return fastai_model
        else:
            mlflow_loaded = mlflow.pyfunc.load_model(model_uri)
            log_info("mlflow_loaded: {0}".format(type(mlflow_loaded)))
            log_info(f"dir(mlflow_loaded): {dir(mlflow_loaded)}")
            model_impl = mlflow_loaded._model_impl
            log_info("model_impl: {0}".format(type(model_impl)))
            log_info(f"dir(model_impl): {dir(model_impl)}")
            internal_model = model_impl.python_model
            log_info(f"internal_model: {type(internal_model)}")
            log_info(f"dir(internal_model): {dir(internal_model)}")
            extracted_model = internal_model._model
            log_info(f"extracted_model: {type(extracted_model)}")
            log_info(f"dir(extracted_model): {dir(extracted_model)}")
            return extracted_model
