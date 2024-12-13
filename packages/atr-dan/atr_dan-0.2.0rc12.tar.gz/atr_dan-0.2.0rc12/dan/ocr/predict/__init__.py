# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Predict on an image using a trained DAN model.
"""

from pathlib import Path

from dan.ocr.predict.attention import Level
from dan.ocr.predict.inference import run
from dan.utils import parse_tokens


def add_predict_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "predict",
        description=__doc__,
        help=__doc__,
    )
    # Required arguments.
    parser.add_argument(
        "--image-dir",
        type=Path,
        help="Path to the folder where the images to predict are stored.",
    )
    parser.add_argument(
        "--model",
        type=Path,
        help="Path to the directory containing the model, the YAML parameters file and the charset file to use for prediction.",
        required=True,
    )
    parser.add_argument(
        "--font",
        type=Path,
        default=Path("fonts/LinuxLibertine.ttf"),
        help="Path to the font file to use for the GIF of the attention map.",
    )
    parser.add_argument(
        "--maximum-font-size",
        type=int,
        default=32,
        help="Maximum font size to use for the GIF of the attention map.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to the output folder.",
        required=True,
    )
    # Optional arguments.
    parser.add_argument(
        "--tokens",
        type=parse_tokens,
        required=False,
        help="Path to a yaml file containing a mapping between starting tokens and end tokens. Needed for entities.",
    )
    parser.add_argument(
        "--image-extension",
        type=str,
        help="The extension of the images in the folder.",
        default=".jpg",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Temperature scaling scalar parameter.",
        required=False,
    )
    parser.add_argument(
        "--confidence-score",
        action="store_true",
        help="Whether to return confidence scores.",
        required=False,
    )
    parser.add_argument(
        "--confidence-score-levels",
        default=[],
        type=Level,
        nargs="+",
        help=f"Levels of confidence scores. Should be a list of any combinaison of {list(map(str, Level))}.",
        required=False,
    )
    parser.add_argument(
        "--attention-map",
        action="store_true",
        help="Whether to plot attention maps.",
        required=False,
    )
    parser.add_argument(
        "--attention-map-level",
        type=Level,
        default=Level.Line,
        help=f"Level to plot the attention maps. Should be in {list(map(str, Level))}.",
        required=False,
    )
    parser.add_argument(
        "--attention-map-scale",
        type=float,
        default=0.5,
        help="Image scaling factor before creating the GIF.",
        required=False,
    )
    parser.add_argument(
        "--alpha-factor",
        help="""Alpha factor that controls how much the attention map is shown
                    to the user during prediction. (typically between .5 and 1)
                    (1 is no change, lower shows more of the attention)""",
        type=float,
        default=0.9,
        required=False,
    )
    parser.add_argument(
        "--color-map",
        help="A matplotlib colormap to use for the attention maps.",
        type=str,
        default="nipy_spectral",
        required=False,
    )
    parser.add_argument(
        "--word-separators",
        default=[" ", "\n"],
        type=str,
        nargs="+",
        help="String separators used to split text into words.",
        required=False,
    )
    parser.add_argument(
        "--line-separators",
        default=["\n"],
        type=str,
        nargs="+",
        help="String separators used to split text into lines.",
        required=False,
    )
    parser.add_argument(
        "--predict-objects",
        action="store_true",
        help="Whether to output objects when plotting attention maps.",
        required=False,
    )
    parser.add_argument(
        "--max-object-height",
        help="Maximum height for predicted objects. If set, grid search segmentation will be applied and width will be normalized to element width.",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--gpu-device",
        help="Use a specific GPU if available.",
        type=int,
        required=False,
    )
    parser.add_argument(
        "--batch-size",
        help="Size of prediction batches.",
        type=int,
        default=1,
        required=False,
    )
    parser.add_argument(
        "--start-token",
        help="Use a specific starting token at the beginning of the prediction. Useful when making predictions on different single pages.",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--use-language-model",
        help="Whether to use an explicit language model to rescore text hypotheses.",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--compile-model",
        help="Whether to compile the model. Recommended to speed up inference.",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--dynamic-mode",
        help="Whether to use the dynamic mode during model compilation. Recommended for prediction on images of variable size.",
        action="store_true",
        required=False,
    )
    parser.set_defaults(func=run)
