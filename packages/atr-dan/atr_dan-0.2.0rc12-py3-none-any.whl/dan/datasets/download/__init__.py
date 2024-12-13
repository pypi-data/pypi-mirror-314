# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Download images of a dataset from a split extracted by DAN
"""

import pathlib

from dan.datasets.download.images import run


def _valid_image_format(value: str):
    im_format = value
    if not im_format.startswith("."):
        im_format = "." + im_format
    return im_format


def add_download_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "download",
        description=__doc__,
        help=__doc__,
    )

    # Required arguments.
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="Path where the `split.json` file is stored and where the data will be generated.",
        required=True,
    )

    parser.add_argument(
        "--max-width",
        type=int,
        help="Images larger than this width will be resized to this width.",
    )

    parser.add_argument(
        "--max-height",
        type=int,
        help="Images larger than this height will be resized to this height.",
    )

    # Formatting arguments
    parser.add_argument(
        "--image-format",
        type=_valid_image_format,
        default=".jpg",
        help="Images will be saved under this format.",
    )

    parser.add_argument(
        "--unknown-token",
        type=str,
        default="⁇",
        help="Token to use to replace character in the validation/test sets that is not included in the training set.",
    )

    parser.set_defaults(func=run)
