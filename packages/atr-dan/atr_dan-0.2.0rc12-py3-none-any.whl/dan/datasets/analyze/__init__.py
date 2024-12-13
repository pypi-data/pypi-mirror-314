# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Analyze dataset and display statistics in markdown format.
"""

from pathlib import Path

from dan.datasets.analyze.statistics import run
from dan.utils import read_json, read_yaml


def add_analyze_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "analyze",
        description=__doc__,
        help=__doc__,
    )
    parser.add_argument(
        "--labels",
        type=Path,
        help="Path to the formatted labels in JSON format.",
        required=True,
    )
    parser.add_argument(
        "--tokens",
        type=read_yaml,
        help="Path to the tokens YAML file.",
        required=False,
    )
    parser.add_argument(
        "--output-file",
        dest="output",
        type=Path,
        help="The statistics will be saved to this file in Markdown format.",
        required=True,
    )
    parser.add_argument(
        "--wandb",
        dest="wandb_params",
        type=read_json,
        help="Keys and values to use to initialise your experiment on W&B.",
    )

    parser.set_defaults(func=run)
