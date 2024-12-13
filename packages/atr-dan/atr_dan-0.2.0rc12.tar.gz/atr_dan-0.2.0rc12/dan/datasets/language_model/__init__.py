# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Build all resources needed for the language model from a split extracted by DAN
"""

import pathlib

from dan.datasets.language_model.build import run


def add_language_model_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "language-model",
        description=__doc__,
        help=__doc__,
    )

    # Required arguments.
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="Path where the `labels.json` and `charset.pkl` files are stored and where the data will be generated.",
        required=True,
    )

    # Formatting arguments
    parser.add_argument(
        "--subword-vocab-size",
        type=int,
        help="Size of the vocabulary to train the sentencepiece subword tokenizer needed for language model.",
        default=1000,
    )

    parser.add_argument(
        "--unknown-token",
        type=str,
        default="⁇",
        help="Token to use to replace character in the validation/test sets that is not included in the training set.",
    )
    parser.add_argument(
        "--tokens",
        type=pathlib.Path,
        help="Mapping between starting tokens and end tokens to extract text with their entities.",
        required=False,
    )

    parser.set_defaults(func=run)
