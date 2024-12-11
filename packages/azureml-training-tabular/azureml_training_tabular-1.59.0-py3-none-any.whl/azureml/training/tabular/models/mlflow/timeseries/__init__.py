# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import os
from typing import Union

import numpy as np
import pandas as pd
import sklearn

try:
    import mlflow
    from mlflow.models import Model
    from mlflow.models.model import MLMODEL_FILE_NAME
    from mlflow.models.signature import ModelSignature
    from mlflow.models.utils import ModelInputExample
    from mlflow.pyfunc import FLAVOR_NAME as PYFUNC_FLAVOR_NAME
    from mlflow.sklearn import SERIALIZATION_FORMAT_PICKLE
    from mlflow.pytorch import _PyTorchWrapper
    from mlflow.tracking._model_registry import DEFAULT_AWAIT_MAX_SLEEP_SECONDS
    from mlflow.utils.model_utils import _get_flavor_configuration

    has_mlflow = True
except ImportError:
    # The mlflow package is not installed.
    # Define dummy classess/functions to make the annotation type check silence.
    class _dummy_class:
        def __init__(self):
            pass

    def _get_flavor_configuration():
        pass

    Model = _dummy_class
    ModelSignature = _dummy_class
    _PyTorchWrapper = _dummy_class
    ModelInputExample = Union[pd.DataFrame, np.ndarray, dict, list]
    MLMODEL_FILE_NAME = "MLmodel"
    PYFUNC_FLAVOR_NAME = "python_function"
    SERIALIZATION_FORMAT_PICKLE = "pickle"
    DEFAULT_AWAIT_MAX_SLEEP_SECONDS = 5 * 60

    has_mlflow = False

# Import azureml modules.
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternal,
    InvalidArgumentType
)
from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.training.tabular.models import mlflow as fc_mlflow
from azureml.training.tabular.models.forecasting_pipeline_wrapper_base import ForecastingPipelineWrapperBase

logger = logging.getLogger(__name__)

# Constants.
MLFLOW_NOT_INSTALLED_WARNING = "The mlflow package is not installed, ignoring {}."
FLAVOR_NAME = "automl-forecasting"
FORECASTING_MODEL_TYPE_KEY = "forecasting_model_type"
SKLEARN_MODEL_TYPE = "fc.model_type.sklearn"
PYTORCH_MODEL_TYPE = "fc.model_type.pytorch"


def log_model(
    fc_model,
    artifact_path,
    conda_env=None,
    code_paths=None,
    serialization_format=SERIALIZATION_FORMAT_PICKLE,
    pickle_module=None,
    signature: ModelSignature = None,
    input_example: ModelInputExample = None,
    await_registration_for=DEFAULT_AWAIT_MAX_SLEEP_SECONDS,
    pip_requirements=None,
    extra_pip_requirements=None,
    metadata=None,
    **kwargs,
):
    """
    Log a Forecasting scikit-learn or pytorch model as an MLflow artifact for the current run.
    Produces an MLflow Model containing the current automl forecasting and inner sklearn or pytorch flavors.

    :param fc_model: scikit-learn or pytorch model to be saved.
    :param artifact_path: Run-relative artifact path.
    :param conda_env: {{ conda_env }}
    :param code_paths: A list of local filesystem paths to Python file dependencies (or directories
                       containing file dependencies). These files are *prepended* to the system
                       path when the model is loaded.
    :param serialization_format: The format in which to serialize the model. This should be one of
                                 the formats listed in
                                 ``mlflow.sklearn.SUPPORTED_SERIALIZATION_FORMATS``. The Cloudpickle
                                 format, ``mlflow.sklearn.SERIALIZATION_FORMAT_CLOUDPICKLE``,
                                 provides better cross-system compatibility by identifying and
                                 packaging code dependencies with the serialized model.
    :param pickle_module: The module that PyTorch should use to serialize ("pickle") the specified
                      ``pytorch_model``. This is passed as the ``pickle_module`` parameter
                      to ``torch.save()``. By default, this module is also used to
                      deserialize ("unpickle") the PyTorch model at load time.
    :param signature: :py:class:`ModelSignature <mlflow.models.ModelSignature>`
                      describes model input and output :py:class:`Schema <mlflow.types.Schema>`.
                      The model signature can be :py:func:`inferred <mlflow.models.infer_signature>`
                      from datasets with valid model input (e.g. the training dataset with target
                      column omitted) and valid model output (e.g. model predictions generated on
                      the training dataset), for example:

                      .. code-block:: python

                        from mlflow.models.signature import infer_signature
                        train = df.drop_column("target_label")
                        predictions = ... # compute model predictions
                        signature = infer_signature(train, predictions)
    :param input_example: Input example provides one or several instances of valid
                          model input. The example can be used as a hint of what data to feed the
                          model. The given example will be converted to a Pandas DataFrame and then
                          serialized to json using the Pandas split-oriented format. Bytes are
                          base64-encoded.
    :param await_registration_for: Number of seconds to wait for the model version to finish
                            being created and is in ``READY`` status. By default, the function
                            waits for five minutes. Specify 0 or None to skip waiting.

    :param pip_requirements: {{ pip_requirements }}
    :param extra_pip_requirements: {{ extra_pip_requirements }}
    :param metadata: Custom metadata dictionary passed to the model and stored in the MLmodel file.

                     .. Note:: Experimental: This parameter may change or be removed in a future
                                             release without warning.
    :param kwargs: kwargs to pass to ``torch.save`` method.
    :return: A :py:class:`ModelInfo <mlflow.models.model.ModelInfo>` instance that contains the
             metadata of the logged model.
    """
    if not has_mlflow:
        logger.warning(MLFLOW_NOT_INSTALLED_WARNING.format("model logging"))
        return None

    try:
        import torch
        is_torch = isinstance(fc_model, torch.nn.Module)
    except Exception:
        is_torch = False

    logger.info("Start logging forecasting mlflow model.")
    if isinstance(fc_model, sklearn.pipeline.Pipeline):
        logger.info("Saving sklearn model to {}.".format(artifact_path))
    elif is_torch:
        logger.info("Saving pytorch model to {}.".format(artifact_path))
    else:
        message = "Unknown model type could not be saved as mlflow."
        raise ClientException._with_error(
            AzureMLError.create(AutoMLInternal, target="models.mlflow.timeseries.log_model", error_details=message)
        )
    mdl_info = Model.log(
        artifact_path=artifact_path,
        flavor=fc_mlflow.timeseries,
        fc_model=fc_model,
        conda_env=conda_env,
        code_paths=code_paths,
        serialization_format=serialization_format,
        pickle_module=pickle_module,
        signature=signature,
        input_example=input_example,
        await_registration_for=await_registration_for,
        pip_requirements=pip_requirements,
        extra_pip_requirements=extra_pip_requirements,
        metadata=metadata,
        **kwargs,
    )
    logger.info("Completed logging forecasting mlflow model.")
    return mdl_info


def save_model(
    fc_model,
    path,
    conda_env=None,
    code_paths=None,
    mlflow_model=None,
    serialization_format=SERIALIZATION_FORMAT_PICKLE,
    pickle_module=None,
    signature: ModelSignature = None,
    input_example: ModelInputExample = None,
    pip_requirements=None,
    extra_pip_requirements=None,
    metadata=None,
    **kwargs,
):
    """
    Save a Forecasting scikit-learn or pytorch model as an MLflow artifact for the current run.
    Produces an MLflow Model containing the current automl forecasting and inner sklearn or pytorch flavors.

    :param fc_model: scikit-learn or pytorch model to be saved.
    :param path: Local path where the model is to be saved.
    :param conda_env: {{ conda_env }}
    :param code_paths: A list of local filesystem paths to Python file dependencies (or directories
                       containing file dependencies). These files are *prepended* to the system
                       path when the model is loaded.
    :param mlflow_model: :py:mod:`mlflow.models.Model` this flavor is being added to.
    :param serialization_format: The format in which to serialize the model. This should be one of
                                 the formats listed in
                                 ``mlflow.sklearn.SUPPORTED_SERIALIZATION_FORMATS``. The Cloudpickle
                                 format, ``mlflow.sklearn.SERIALIZATION_FORMAT_CLOUDPICKLE``,
                                 provides better cross-system compatibility by identifying and
                                 packaging code dependencies with the serialized model.
    :param pickle_module: The module that PyTorch should use to serialize ("pickle") the specified
                          ``pytorch_model``. This is passed as the ``pickle_module`` parameter
                          to ``torch.save()``. By default, this module is also used to
                          deserialize ("unpickle") the PyTorch model at load time.

    :param signature: :py:class:`ModelSignature <mlflow.models.ModelSignature>`
                      describes model input and output :py:class:`Schema <mlflow.types.Schema>`.
                      The model signature can be :py:func:`inferred <mlflow.models.infer_signature>`
                      from datasets with valid model input (e.g. the training dataset with target
                      column omitted) and valid model output (e.g. model predictions generated on
                      the training dataset), for example:

                      .. code-block:: python

                        from mlflow.models.signature import infer_signature
                        train = df.drop_column("target_label")
                        predictions = ... # compute model predictions
                        signature = infer_signature(train, predictions)
    :param input_example: Input example provides one or several instances of valid
                          model input. The example can be used as a hint of what data to feed the
                          model. The given example will be converted to a Pandas DataFrame and then
                          serialized to json using the Pandas split-oriented format. Bytes are
                          base64-encoded.
    :param pip_requirements: {{ pip_requirements }}
    :param extra_pip_requirements: {{ extra_pip_requirements }}
    :param metadata: Custom metadata dictionary passed to the model and stored in the MLmodel file.

    :param kwargs: kwargs to pass to sklearn or torch flaver model save methods.

    """
    if not has_mlflow:
        logger.warning(MLFLOW_NOT_INSTALLED_WARNING.format("model saving"))
        return

    try:
        import torch
        is_torch = isinstance(fc_model, torch.nn.Module)
    except Exception:
        is_torch = False

    logger.info("Start saving mlflow model.")
    fc_model_type = ""
    if isinstance(fc_model, sklearn.pipeline.Pipeline):
        # For the sklearn model/pipeline call the sklearn flavor's save_model() to do the actual
        # pyfunc model saving work.
        mlflow.sklearn.save_model(
            sk_model=fc_model,
            path=path,
            conda_env=conda_env,
            code_paths=code_paths,
            mlflow_model=mlflow_model,
            serialization_format=serialization_format,
            signature=signature,
            input_example=input_example,
            pip_requirements=pip_requirements,
            extra_pip_requirements=extra_pip_requirements,
            metadata=metadata
        )
        fc_model_type = SKLEARN_MODEL_TYPE
    elif is_torch:
        # For the pytorch model call the pytorch flavor's save_model() to do the actual
        # pyfunc model saving work.
        mlflow.pytorch.save_model(
            pytorch_model=fc_model,
            path=path,
            conda_env=conda_env,
            code_paths=code_paths,
            mlflow_model=mlflow_model,
            pickle_module=pickle_module,
            signature=signature,
            input_example=input_example,
            pip_requirements=pip_requirements,
            extra_pip_requirements=extra_pip_requirements,
            metadata=metadata,
            **kwargs
        )
        fc_model_type = PYTORCH_MODEL_TYPE
    else:
        message = "Unknown model type could not be saved as mlflow."
        raise ClientException._with_error(
            AzureMLError.create(AutoMLInternal, target="models.mlflow.timeseries.log_model", error_details=message)
        )

    # Override the 'module_loader' of python_function default flavor to this forecasting mlflow flavor module
    # for the pyfunc model loading.
    default_python_function_flavor_params = mlflow_model.flavors[PYFUNC_FLAVOR_NAME]
    if mlflow.pyfunc.MAIN not in default_python_function_flavor_params:
        logger.warning(f"The {mlflow.pyfunc.MAIN} was not properly set by sklearn or pytorch flavor.")
    default_python_function_flavor_params[mlflow.pyfunc.MAIN] = "azureml.training.tabular.models.mlflow.timeseries"

    # Add the forecasting flavor.
    mlflow_model.add_flavor(
        FLAVOR_NAME,
        forecasting_model_type=fc_model_type
    )

    # Save the MLflow model with forecasting flavor config and module loader info.
    mlflow_model.save(os.path.join(path, MLMODEL_FILE_NAME))
    logger.info("Completed saving mlflow model.")


class _ForecastingPyfuncModelWrapper:
    """
    Wrapper class that creates a predict function.
    The predict function will preprocess the given input and call the inner forecasting model's forecast method.
    """

    def __init__(self, forecasting_model: ForecastingPipelineWrapperBase):
        if forecasting_model.__class__.__name__ == '_SklearnModelWrapper':
            self.forecasting_model = forecasting_model.sklearn_model
        else:
            self.forecasting_model = forecasting_model

    def predict(self, data):
        logger.info("Start the forecast with the pyfunc forecasting model wrapper.")

        # Check the input data type to ensure it's a pandas DataFrame first.
        if not isinstance(data, pd.DataFrame):
            raise ForecastingDataException._with_error(
                AzureMLError.create(
                    InvalidArgumentType,
                    target='data',
                    reference_code=ReferenceCodes._TSDF_INVALID_ARG_FC_PIPELINE_X_PRED,
                    argument='data',
                    expected_types='pandas.DataFrame',
                    actual_type=str(type(data))
                )
            )

        X_pred = data.reset_index(drop=True)
        y_pred = None
        # Split the X and y from input if the input contains the target column.
        user_target_col_name = self.forecasting_model.user_target_column_name
        if user_target_col_name is not None and user_target_col_name in data.columns.values:
            y_pred = X_pred.pop(user_target_col_name).values

        # Forecast.
        y_res, _ = self.forecasting_model.forecast(X_pred=X_pred, y_pred=y_pred, ignore_data_errors=True)
        logger.info("Forecast ended.")
        return y_res


def _load_pyfunc(path, model_config=None):
    """
    Load PyFunc implementation. Called by ``pyfunc.load_model``.

    :param path: Local filesystem path to the MLflow Model with the automl forecasting flavor.
    """

    model_configuration_path = os.path.join(path, MLMODEL_FILE_NAME)
    art_folder_path = path
    if not os.path.exists(model_configuration_path):
        # Try get the flavor config from the path given by the pyfunc load_model() method, if it doesn't exists
        # it means this is the './data' sub folder of the mlflow artifact folder.
        art_folder_path = os.path.dirname(art_folder_path)

    flavor_conf = _get_flavor_configuration(model_path=art_folder_path, flavor_name=FLAVOR_NAME)
    fc_model_type = flavor_conf[FORECASTING_MODEL_TYPE_KEY]
    fc_model = None
    if fc_model_type == SKLEARN_MODEL_TYPE:
        fc_model = mlflow.sklearn._load_pyfunc(path)
    elif fc_model_type == PYTORCH_MODEL_TYPE:
        if model_config is None:
            fc_model = mlflow.pytorch._load_pyfunc(path)
        else:
            fc_model = mlflow.pytorch._load_pyfunc(path, model_config)
        if isinstance(fc_model, _PyTorchWrapper):
            # The mlflow.pytorch module uses a pytorch wrapper class to hold the inner actual torch model.
            fc_model = fc_model.pytorch_model
    else:
        message = "Unknown forecasting model type could not be loaded."
        raise ClientException._with_error(
            AzureMLError.create(AutoMLInternal, target="models.mlflow.timeseries._load_pyfunc", error_details=message)
        )
    return _ForecastingPyfuncModelWrapper(forecasting_model=fc_model)
