# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Generate the YAML file containing entities and their token(s) to train a DAN model
"""
from pathlib import Path

from dan.datasets.tokens.generate import run


def add_tokens_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "tokens",
        description=__doc__,
        help=__doc__,
    )
    parser.add_argument(
        "entities",
        type=Path,
        help="Path to a YAML file containing the extracted entities.",
    )
    parser.add_argument(
        "--end-tokens",
        action="store_true",
        help="Whether to generate end tokens along with starting tokens.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=Path("tokens.yml"),
        required=False,
        help="Path to a YAML file to save the entities and their token(s).",
    )

    parser.set_defaults(func=run)
