# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""PyfuncModel class to load mlflow models into memory."""

try:
    from mlflow.pyfunc import PythonModel
    mlflow_import_error = False
except ImportError:
    PythonModel = object
    mlflow_import_error = True


class PyfuncModel(PythonModel):
    """PyfuncModel class to load mlflow models into memory."""

    def __init__(self, my_model):
        """Initialize PyfuncModel.

        :param my_model: The model to wrap.
        :type my_model: object
        """
        if mlflow_import_error:
            error = "mlflow not installed, cannot use PyfuncModel wrapper"
            raise ImportError(error)
        self._model = my_model
