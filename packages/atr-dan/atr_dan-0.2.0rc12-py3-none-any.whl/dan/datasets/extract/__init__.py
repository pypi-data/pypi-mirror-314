# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Extract dataset from Arkindex using a corpus export.
"""

import argparse
import pathlib
from uuid import UUID

from dan.datasets.extract.arkindex import run

MANUAL_SOURCE = "manual"


def parse_source(source) -> str | bool:
    if source == MANUAL_SOURCE:
        return False

    try:
        UUID(source)
    except ValueError:
        raise argparse.ArgumentTypeError(f"`{source}` is not a valid UUID.")

    return source


def validate_char(char):
    if len(char) != 1:
        raise argparse.ArgumentTypeError(
            f"`{char}` (of length {len(char)}) is not a valid character. Must be a string of length 1."
        )

    return char


def add_extract_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "extract",
        description=__doc__,
        help=__doc__,
    )

    # Required arguments.
    parser.add_argument(
        "database",
        type=pathlib.Path,
        help="Path where the data were exported from Arkindex.",
    )
    parser.add_argument(
        "--dataset-id",
        nargs="+",
        type=UUID,
        help="ID of the dataset to extract from Arkindex.",
        required=True,
        dest="dataset_ids",
    )
    parser.add_argument(
        "--element-type",
        nargs="+",
        type=str,
        help="Type of elements to retrieve.",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="Path where the data will be generated.",
        required=True,
    )

    # Optional arguments.
    parser.add_argument(
        "--entity-separators",
        type=validate_char,
        nargs="+",
        help="""
            Removes all text that does not appear in an entity or in the list of given ordered characters.
            If several separators follow each other, keep only the first to appear in the list.
            Do not give any arguments to keep the whole text.
        """,
    )

    parser.add_argument(
        "--tokens",
        type=pathlib.Path,
        help="Mapping between starting tokens and end tokens to extract text with their entities.",
        required=False,
    )

    parser.add_argument(
        "--transcription-worker-versions",
        type=parse_source,
        nargs="+",
        help=f"Filter transcriptions by worker_version. Use {MANUAL_SOURCE} for manual filtering.",
        default=[],
    )
    parser.add_argument(
        "--entity-worker-versions",
        type=parse_source,
        nargs="+",
        help=f"Filter transcriptions entities by worker_version. Use {MANUAL_SOURCE} for manual filtering.",
        default=[],
    )
    parser.add_argument(
        "--transcription-worker-runs",
        type=parse_source,
        nargs="+",
        help=f"Filter transcriptions by worker_run. Use {MANUAL_SOURCE} for manual filtering.",
        default=[],
    )
    parser.add_argument(
        "--entity-worker-runs",
        type=parse_source,
        nargs="+",
        help=f"Filter transcriptions entities by worker_run. Use {MANUAL_SOURCE} for manual filtering.",
        default=[],
    )

    # Formatting arguments
    parser.add_argument(
        "--keep-spaces",
        action="store_true",
        help="Do not remove beginning, ending and consecutive spaces in transcriptions.",
    )

    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Also extract data from element with no transcription.",
    )

    parser.set_defaults(func=run)
