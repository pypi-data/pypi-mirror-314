# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Evaluate a trained DAN model.
"""

import json
import logging
import random
from argparse import ArgumentTypeError
from itertools import chain
from operator import attrgetter
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch
import torch.multiprocessing as mp
from edlib import align, getNiceAlignment
from nerval.evaluate import evaluate
from nerval.parse import parse_bio
from nerval.utils import TABLE_HEADER as NERVAL_TABLE_HEADER
from nerval.utils import print_results
from prettytable import MARKDOWN, PrettyTable

from dan.bio import convert
from dan.ocr import wandb
from dan.ocr.manager.metrics import Inference
from dan.ocr.manager.training import Manager
from dan.ocr.utils import add_metrics_table_row, create_metrics_table, update_config
from dan.utils import parse_tokens, read_json

logger = logging.getLogger(__name__)

NERVAL_THRESHOLD = 0.30
NB_WORST_PREDICTIONS = 5

EMPTY_STRING = "∅"


def parse_threshold(value: str) -> float:
    """
    Check that the string passed as parameter is a correct floating point number between 0 and 1
    """
    try:
        value = float(value)
    except ValueError:
        raise ArgumentTypeError("Must be a floating point number.")

    if value < 0 or value > 1:
        raise ArgumentTypeError("Must be between 0 and 1.")

    return value


def add_evaluate_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "evaluate",
        description=__doc__,
        help=__doc__,
    )

    parser.add_argument(
        "--config",
        type=read_json,
        required=True,
        help="Configuration file.",
    )

    parser.add_argument(
        "--nerval-threshold",
        help="Distance threshold for the match between gold and predicted entity during Nerval evaluation.",
        default=NERVAL_THRESHOLD,
        type=parse_threshold,
    )

    parser.add_argument(
        "--output-json",
        help="Where to save evaluation results in JSON format.",
        default=None,
        type=Path,
    )

    parser.set_defaults(func=run)


def print_worst_predictions(all_inferences: Dict[str, List[Inference]]):
    table_header, table_values = (
        [
            "Image name",
            "WER",
            "Alignment between ground truth - prediction",
        ],
        [],
    )

    worst_inferences = sorted(
        chain.from_iterable(all_inferences.values()),
        key=attrgetter("wer"),
        reverse=True,
    )[:NB_WORST_PREDICTIONS]
    for inference in worst_inferences:
        if not inference.ground_truth:
            logger.warning(
                f"Ground truth is empty for {inference.image}. `{EMPTY_STRING}` will be displayed"
            )

        if not inference.prediction:
            logger.warning(
                f"Prediction is empty for {inference.image}. `{EMPTY_STRING}` will be displayed"
            )

        alignment = getNiceAlignment(
            align(
                inference.ground_truth or EMPTY_STRING,
                inference.prediction or EMPTY_STRING,
                task="path",
            ),
            inference.ground_truth or EMPTY_STRING,
            inference.prediction or EMPTY_STRING,
        )
        alignment_str = f'{alignment["query_aligned"]}\n{alignment["matched_aligned"]}\n{alignment["target_aligned"]}'
        table_values.append(
            [inference.image, round(inference.wer * 100, 2), alignment_str]
        )

    # Display/Log tables
    print(f"\n#### {NB_WORST_PREDICTIONS} worst prediction(s)\n")

    table = PrettyTable(field_names=table_header)
    table.set_style(MARKDOWN)
    table.add_rows(table_values)
    print(table)

    wandb.table(
        f"evaluation/{NB_WORST_PREDICTIONS}_worst_predictions",
        columns=table_header,
        data=table_values,
    )


def eval_nerval(
    all_inferences: Dict[str, List[Inference]],
    tokens: Path,
    threshold: float,
):
    print("\n#### Nerval evaluation")

    def inferences_to_parsed_bio(attr: str):
        bio_values = []
        for inference in inferences:
            value = getattr(inference, attr)
            bio_value = convert(value, ner_tokens=tokens)
            bio_values.extend(bio_value.split("\n"))

        # Parse this BIO format
        return parse_bio(bio_values)

    # Evaluate with Nerval
    tokens = parse_tokens(tokens)
    for split_name, inferences in all_inferences.items():
        ground_truths = inferences_to_parsed_bio("ground_truth")
        predictions = inferences_to_parsed_bio("prediction")

        if not (ground_truths and predictions):
            continue

        scores = {
            key: {
                k: round(value * 100, 2)
                if k in ["P", "R", "F1"] and value is not None
                # Value can be None when
                # no entity is predicted for a specific entity type
                # there is no entity in the labels for a specific entity type
                else (value or 0)
                for k, value in values.items()
            }
            for key, values in evaluate(ground_truths, predictions, threshold).items()
        }

        # Display/Log tables
        print(f"\n##### {split_name}\n")
        metrics_values = print_results(scores)
        wandb.table(
            f"evaluation/nerval/{split_name}",
            columns=NERVAL_TABLE_HEADER,
            data=metrics_values,
        )


def eval(
    rank,
    config: dict,
    nerval_threshold: float,
    output_json: Path | None,
    mlflow_logging: bool,
):
    torch.manual_seed(0)
    torch.cuda.manual_seed(0)
    np.random.seed(0)
    random.seed(0)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

    config["training"]["device"]["ddp_rank"] = rank

    # Load best checkpoint
    config["training"]["load_epoch"] = "best"

    model = Manager(config)
    model.load_model()

    metric_names = [
        "cer",
        "cer_no_token",
        "wer",
        "wer_no_punct",
        "wer_no_token",
        "time",
    ]
    if config["dataset"]["tokens"] is not None:
        metric_names.append("ner")

    metrics_table = create_metrics_table(metric_names)
    metrics_values, all_inferences = [], {}

    for dataset_name in config["dataset"]["datasets"]:
        for set_name in ["train", "val", "test"]:
            logger.info(f"Evaluating on set `{set_name}`")
            metrics, inferences = model.evaluate(
                "{}-{}".format(dataset_name, set_name),
                [
                    (dataset_name, set_name),
                ],
                metric_names,
                mlflow_logging=mlflow_logging,
            )

            metrics_values.append(
                add_metrics_table_row(metrics_table, set_name, metrics)
            )
            all_inferences[set_name] = inferences

    # Display/Log tables
    print("\n#### DAN evaluation\n")
    print(metrics_table)
    wandb.table(
        "evaluation/dan", columns=metrics_table.field_names, data=metrics_values
    )

    if "ner" in metric_names:
        eval_nerval(
            all_inferences,
            tokens=config["dataset"]["tokens"],
            threshold=nerval_threshold,
        )

    print_worst_predictions(all_inferences)

    # Save to JSON
    if output_json is not None:
        output_json.write_text(json.dumps(all_inferences, indent=2))

        if config.get("wandb", {}).get("inferences"):
            artifact = wandb.artifact(
                name=f"run-{wandb.run_id()}-evaluation",
                type="json",
                description="Evaluation metrics",
            )
            wandb.log_artifact(artifact, local_path=output_json, name=output_json.name)


def run(config: dict, nerval_threshold: float, output_json: Path | None):
    update_config(config)

    # Start "Weights & Biases" as soon as possible
    wandb.init(
        wandb_params=config.get("wandb", {}).get("init", {}),
        config={wandb.Config.EVALUATION.value: config},
        output_folder=config["training"]["output_folder"],
    )

    mlflow_logging = bool(config.get("mlflow"))

    if mlflow_logging:
        logger.info("MLflow logging enabled")

    if (
        config["training"]["device"]["use_ddp"]
        and config["training"]["device"]["force"] in [None, "cuda"]
        and torch.cuda.is_available()
    ):
        mp.spawn(
            eval,
            args=(config, nerval_threshold, output_json, mlflow_logging),
            nprocs=config["training"]["device"]["nb_gpu"],
        )
    else:
        eval(0, config, nerval_threshold, output_json, mlflow_logging)
