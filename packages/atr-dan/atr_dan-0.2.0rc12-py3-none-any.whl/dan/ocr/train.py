# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import json
import logging
import random
import sys
from copy import deepcopy
from itertools import pairwise

import numpy as np
import torch
import torch.multiprocessing as mp
from torch.cuda import OutOfMemoryError
from torch.multiprocessing.spawn import ProcessExitedException

from dan.ocr import wandb
from dan.ocr.manager.training import Manager
from dan.ocr.mlflow import MLFLOW_AVAILABLE
from dan.ocr.utils import build_batch_sizes, update_config
from dan.utils import MLflowNotInstalled

if MLFLOW_AVAILABLE:
    import mlflow

    from dan.ocr.mlflow import make_mlflow_request, start_mlflow_run


logger = logging.getLogger(__name__)

# Special exit code used when the training stopped because of a `torch.cuda.OutOfMemoryError`
EXIT_CODE_OUT_OF_MEMORY_ERROR = 142


def train(rank, params, mlflow_logging=False):
    # Start "Weights & Biases" as soon as possible
    wandb.init(
        wandb_params=params.get("wandb", {}).get("init", {}),
        config={wandb.Config.TRAINING.value: params},
        output_folder=params["training"]["output_folder"],
    )

    torch.manual_seed(0)
    torch.cuda.manual_seed(0)
    np.random.seed(0)
    random.seed(0)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

    params["training"]["device"]["ddp_rank"] = rank
    model = Manager(params)
    model.load_model()

    if params["dataset"]["tokens"] is not None:
        if "ner" not in params["training"]["metrics"]["train"]:
            params["training"]["metrics"]["train"].append("ner")
        if "ner" not in params["training"]["metrics"]["eval"]:
            params["training"]["metrics"]["eval"].append("ner")

    if mlflow_logging:
        logger.info("MLflow logging enabled")

    try:
        model.train(mlflow_logging=mlflow_logging)
    except OutOfMemoryError as e:
        logger.error(repr(e))
        sys.exit(EXIT_CODE_OUT_OF_MEMORY_ERROR)


def serialize_config(config):
    """
    Make every field of the configuration JSON-Serializable and remove sensitive information.

    - Classes are transformed using their name attribute
    - Functions are casted to strings
    """
    # Create a copy of the original config without erase it
    serialized_config = deepcopy(config)

    # Remove credentials to the config
    serialized_config["mlflow"]["s3_endpoint_url"] = ""
    serialized_config["mlflow"]["tracking_uri"] = ""
    serialized_config["mlflow"]["aws_access_key_id"] = ""
    serialized_config["mlflow"]["aws_secret_access_key"] = ""

    # Get the name of the class
    serialized_config["model"]["models"]["encoder"] = serialized_config["model"][
        "models"
    ]["encoder"].__name__
    serialized_config["model"]["models"]["decoder"] = serialized_config["model"][
        "models"
    ]["decoder"].__name__
    serialized_config["training"]["optimizers"]["all"]["class"] = serialized_config[
        "training"
    ]["optimizers"]["all"]["class"].__name__

    # Cast the functions to str
    serialized_config["dataset"]["config"]["augmentation"] = str(
        serialized_config["dataset"]["config"]["augmentation"]
    )
    serialized_config["training"]["nb_gpu"] = str(
        serialized_config["training"]["nb_gpu"]
    )

    return serialized_config


def run(config: dict):
    """
    Main program, training a new model, using a valid configuration
    """
    names = list(config["dataset"]["datasets"].keys())
    # We should only have one dataset
    assert len(names) == 1, f"Found {len(names)} datasets but only one is expected"

    dataset_name = names.pop()
    update_config(config)

    if config.get("mlflow"):
        if not MLFLOW_AVAILABLE:
            logger.error(
                "Cannot log to MLflow. Please install the `mlflow` extra requirements."
            )
            raise MLflowNotInstalled()

        labels_path = config["dataset"]["datasets"][dataset_name] / "labels.json"
        with start_mlflow_run(config["mlflow"]) as (mlflow_run, created):
            if created:
                logger.info(f"Started MLflow run with ID ({mlflow_run.info.run_id})")
            else:
                logger.info(f"Resumed MLflow run with ID ({mlflow_run.info.run_id})")

            make_mlflow_request(
                mlflow_method=mlflow.set_tags, tags={"Dataset": dataset_name}
            )
            # Get the labels json file
            labels_artifact = json.loads(labels_path.read_text())

            # Log MLflow artifacts
            for artifact, filename in [
                (serialize_config(config), "config.json"),
                (labels_artifact, "labels.json"),
            ]:
                make_mlflow_request(
                    mlflow_method=mlflow.log_dict,
                    dictionary=artifact,
                    artifact_file=filename,
                )

    initial_batch_size = config["training"]["data"]["batch_size"]
    batch_sizes = list(build_batch_sizes(initial_batch_size))
    logger.info(
        f"Training will start with a batch size of {initial_batch_size}. "
        f"If training requires too much memory, it will be stopped and will be restarted with a smaller batch: {batch_sizes[1:]}."
    )
    for batch_size, next_batch_size in pairwise(batch_sizes + [None]):
        config["training"]["data"]["batch_size"] = batch_size
        try:
            mp.spawn(
                train,
                args=(config, bool(config.get("mlflow"))),
                nprocs=(
                    config["training"]["device"]["nb_gpu"]
                    if (
                        config["training"]["device"]["use_ddp"]
                        and config["training"]["device"]["force"] in [None, "cuda"]
                        and torch.cuda.is_available()
                    )
                    else 1
                ),
            )
            return
        except ProcessExitedException as e:
            # Training stopped for another reason
            if e.exit_code != EXIT_CODE_OUT_OF_MEMORY_ERROR:
                raise

            # No more batch size available
            if not next_batch_size:
                raise Exception(
                    "torch.cuda.OutOfMemoryError: No more batch size available"
                )

            logger.warning(
                f"Failed to train with batch size of {batch_size}. Trying with smaller batch size of {next_batch_size}..."
            )
