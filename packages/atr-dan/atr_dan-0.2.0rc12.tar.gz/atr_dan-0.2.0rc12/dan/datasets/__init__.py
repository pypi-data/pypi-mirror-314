# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Preprocess datasets for training.
"""

from dan.datasets.analyze import add_analyze_parser
from dan.datasets.download import add_download_parser
from dan.datasets.entities import add_entities_parser
from dan.datasets.extract import add_extract_parser
from dan.datasets.language_model import add_language_model_parser
from dan.datasets.tokens import add_tokens_parser


def add_dataset_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "dataset",
        description=__doc__,
        help=__doc__,
    )
    subcommands = parser.add_subparsers(metavar="subcommand")

    add_extract_parser(subcommands)
    add_download_parser(subcommands)
    add_analyze_parser(subcommands)
    add_entities_parser(subcommands)
    add_tokens_parser(subcommands)
    add_language_model_parser(subcommands)
