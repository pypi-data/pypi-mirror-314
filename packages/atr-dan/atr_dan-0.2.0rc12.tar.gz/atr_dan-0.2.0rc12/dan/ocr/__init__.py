# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Train a new DAN model.
"""


from dan.ocr.evaluate import add_evaluate_parser  # noqa
from dan.ocr.predict import add_predict_parser  # noqa
from dan.ocr.train import run
from dan.utils import read_json


def add_train_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "train",
        description=__doc__,
        help=__doc__,
    )

    parser.add_argument(
        "--config",
        type=read_json,
        required=True,
        help="Configuration file.",
    )

    parser.set_defaults(func=run)
