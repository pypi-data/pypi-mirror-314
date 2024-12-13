# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import argparse
import errno

from dan.bio import add_convert_bio_parser
from dan.datasets import add_dataset_parser
from dan.ocr import add_evaluate_parser, add_predict_parser, add_train_parser


def get_parser():
    parser = argparse.ArgumentParser(prog="teklia-dan")
    subcommands = parser.add_subparsers(metavar="subcommand")

    add_convert_bio_parser(subcommands)
    add_dataset_parser(subcommands)
    add_train_parser(subcommands)
    add_evaluate_parser(subcommands)
    add_predict_parser(subcommands)
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    if "func" in args:
        # Run the subcommand's function
        try:
            status = args.pop("func")(**args)
            parser.exit(status=status)
        except KeyboardInterrupt:
            # Just quit silently on ^C instead of displaying a long traceback
            parser.exit(status=errno.EOWNERDEAD)
    else:
        parser.error("A subcommand is required.")
