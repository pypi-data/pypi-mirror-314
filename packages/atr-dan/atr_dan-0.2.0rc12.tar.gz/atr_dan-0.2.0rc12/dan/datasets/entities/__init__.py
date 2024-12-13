# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Extract entities from Arkindex using a corpus export.
"""
from pathlib import Path

from dan.datasets.entities.extract import run


def add_entities_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "entities",
        description=__doc__,
        help=__doc__,
    )
    parser.add_argument(
        "database",
        type=Path,
        help="Path where the data were exported from Arkindex.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=Path("entities.yml"),
        required=False,
        help="Path to a YAML file to save the extracted entities.",
    )
    parser.set_defaults(func=run)
