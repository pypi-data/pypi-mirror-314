# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import functools
import logging
import os
from contextlib import contextmanager

import requests

logger = logging.getLogger(__name__)

try:
    import mlflow
    from mlflow.environment_variables import MLFLOW_HTTP_REQUEST_MAX_RETRIES

    MLFLOW_AVAILABLE = True
    logger.info("MLflow logging is available.")
except ImportError:
    MLFLOW_AVAILABLE = False


def mlflow_required(func):
    """
    Always check that MLflow is available before executing the function.
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not MLFLOW_AVAILABLE:
            return
        return func(self, *args, **kwargs)

    return wrapper


@mlflow_required
def make_mlflow_request(mlflow_method, *args, **kwargs):
    """
    Encapsulate MLflow HTTP requests to prevent them from crashing the whole training process.
    """
    try:
        mlflow_method(*args, **kwargs)
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Call to `{str(mlflow_method)}` failed with error: {str(e)}")


@mlflow_required
def setup_environment(config: dict):
    """
    Get the necessary variables from the config file and put them in the environment variables

    :param config: dict, the config of the model
    """
    needed_variables = {
        "MLFLOW_S3_ENDPOINT_URL": "s3_endpoint_url",
        "MLFLOW_TRACKING_URI": "tracking_uri",
        "AWS_ACCESS_KEY_ID": "aws_access_key_id",
        "AWS_SECRET_ACCESS_KEY": "aws_secret_access_key",
    }
    for variable_name, config_key in needed_variables.items():
        if config_key in config:
            os.environ[variable_name] = config[config_key]

    # Check max retry setting
    max_retries = MLFLOW_HTTP_REQUEST_MAX_RETRIES.get()
    if max_retries and int(max_retries) <= 1:
        logger.warning(
            f"The maximum number of retries for MLflow HTTP requests is set to {max_retries}, which is low. Consider using a higher value."
        )


@mlflow_required
def logging_metrics(
    display_values: dict,
    step: str,
    epoch: int,
    mlflow_logging: bool = False,
    is_master: bool = False,
):
    """
    Log dictionary metrics in the Metrics section of MLflow

    :param display_values: dict, the dictionary containing the metrics to publish on MLflow
    :param step: str, the step for which the metrics are to be published on Metrics section (ex: train, val, test). This will allow a better display on MLflow.
    :param epoch: int, the current epoch.
    :param mlflow_logging: bool, allows you to verify that you have the authorization to log on MLflow, defaults to False
    :param is_master: bool, makes sure you're on the right thread, defaults to False
    """
    if mlflow_logging and is_master:
        make_mlflow_request(
            mlflow_method=mlflow.log_metrics,
            metrics={f"{step}_{name}": value for name, value in display_values.items()},
            step=epoch,
        )


@mlflow_required
def logging_tags_metrics(
    display_values: dict,
    step: str,
    mlflow_logging: bool = False,
    is_master: bool = False,
):
    """
    Log dictionary metrics in the Tags section of MLflow

    :param display_values: dict, the dictionary containing the metrics to publish on MLflow
    :param step: str, the step for which the metrics are to be published on Tags section (ex: train, val, test). This will allow a better display on MLflow.
    :param mlflow_logging: bool, allows you to verify that you have the authorization to log on MLflow, defaults to False
    :param is_master: bool, makes sure you're on the right thread, defaults to False
    """
    if mlflow_logging and is_master:
        make_mlflow_request(
            mlflow_method=mlflow.set_tags,
            tags={f"{step}_{name}": value for name, value in display_values.items()},
        )


@mlflow_required
@contextmanager
def start_mlflow_run(config: dict):
    """
    Create an MLflow execution context with the parameters contained in the config file.

    Yields the active MLflow run, as well as a boolean saying whether a new one was created.

    :param config: dict, the config of the model
    """

    # Set needed variables in environment
    setup_environment(config)

    run_name, run_id = config.get("run_name"), config.get("run_id")

    if run_id:
        logger.info(f"Will resume run ({run_id}).")

        if run_name:
            logger.warning(
                "Run_name will be ignored since you specified a run_id to resume from."
            )

    # Set experiment from config
    experiment_id = config.get("experiment_id")
    assert experiment_id, "Missing MLflow experiment ID in the configuration"

    # Start run
    yield (
        mlflow.start_run(run_id=run_id, run_name=run_name, experiment_id=experiment_id),
        run_id is None,
    )
    mlflow.end_run()
