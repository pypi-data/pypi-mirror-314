# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from statistics import mean
from typing import Dict, Iterator, List, Optional

import torch
from numpy import int32, ndarray
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont
from prettytable import MARKDOWN, PrettyTable
from torch.optim import Adam

from dan.ocr.decoder import GlobalHTADecoder
from dan.ocr.encoder import FCN_Encoder
from dan.ocr.transforms import Preprocessing

logger = logging.getLogger(__name__)

METRICS_TABLE_HEADER = {
    "cer": "CER (HTR-NER)",
    "cer_no_token": "CER (HTR)",
    "wer": "WER (HTR-NER)",
    "wer_no_token": "WER (HTR)",
    "wer_no_punct": "WER (HTR no punct)",
    "ner": "NER",
}
REVERSE_HEADER = {column: metric for metric, column in METRICS_TABLE_HEADER.items()}


def update_config(config: dict):
    """
    Complete the fields that are not JSON serializable.
    """

    # .dataset.datasets cast all values to Path
    config["dataset"]["datasets"] = {
        name: Path(path) for name, path in config["dataset"]["datasets"].items()
    }

    # .model.encoder.class = FCN_ENCODER
    config["model"]["encoder"]["class"] = FCN_Encoder

    # .model.decoder.class = GlobalHTADecoder
    config["model"]["decoder"]["class"] = GlobalHTADecoder

    # .model.lm.path to Path
    if config["model"].get("lm", {}).get("path"):
        config["model"]["lm"]["path"] = Path(config["model"]["lm"]["path"])

    # Update preprocessing type
    for prepro in config["training"]["data"]["preprocessings"]:
        prepro["type"] = Preprocessing(prepro["type"])

    # .training.output_folder to Path
    config["training"]["output_folder"] = Path(config["training"]["output_folder"])

    if config["training"]["transfer_learning"]:
        # .training.transfer_learning.encoder[1]
        config["training"]["transfer_learning"]["encoder"][1] = Path(
            config["training"]["transfer_learning"]["encoder"][1]
        )

        # .training.transfer_learning.decoder[1]
        config["training"]["transfer_learning"]["decoder"][1] = Path(
            config["training"]["transfer_learning"]["decoder"][1]
        )

    # Parse optimizers
    for optimizer_setup in config["training"]["optimizers"].values():
        # Only supported optimizer is Adam
        optimizer_setup["class"] = Adam

    # set nb_gpu if not present
    if config["training"]["device"]["nb_gpu"] is None:
        config["training"]["device"]["nb_gpu"] = torch.cuda.device_count()


def build_batch_sizes(batch_size: int) -> Iterator[int]:
    """
    Build a list of integers by dividing the previous one by 2.
    If the resulting integer is not even, take the nearest multiple of 4.
    """
    # The minimum batch size is always 1
    if batch_size < 1:
        return

    yield batch_size

    next_batch_size = batch_size // 2
    next_batch_size = (
        # If the result is not even, we take the nearest multiple of 4
        next(
            filter(
                lambda potential_next_batch_size: not potential_next_batch_size % 4,
                [next_batch_size - 1, next_batch_size, next_batch_size + 1],
            )
        )
        if next_batch_size % 2 and next_batch_size != 1
        else next_batch_size
    )

    yield from build_batch_sizes(next_batch_size)


def create_metrics_table(metrics: List[str]) -> PrettyTable:
    """
    Create a Markdown table to display metrics in (CER, WER, NER, etc)
    for each evaluated split.
    """
    table = PrettyTable(
        field_names=["Split"]
        + [title for metric, title in METRICS_TABLE_HEADER.items() if metric in metrics]
    )
    table.set_style(MARKDOWN)

    return table


def add_metrics_table_row(
    table: PrettyTable, split: str, metrics: Optional[Dict[str, int | float]]
) -> list[str]:
    """
    Add a row to an existing metrics Markdown table for the currently evaluated split.
    To create such table please refer to
    [create_metrics_table][dan.ocr.utils.create_metrics_table] function.
    """
    row = [split]
    for column in table.field_names:
        if column not in REVERSE_HEADER:
            continue

        metric_name = REVERSE_HEADER[column]
        metric_value = metrics.get(metric_name)
        row.append(round(metric_value * 100, 2) if metric_value is not None else "−")

    table.add_row(row)
    return row


def load_font(path: Path, size: int):
    """
    Load the font.
    :param path: Path to the font.
    :param size: Size of the font.
    """
    return ImageFont.truetype(path, size)


def search_font_size(
    image: Image,
    font: Path,
    maximum_font_size: int,
    text: str,
    width: int | None = None,
    height: int | None = None,
) -> int:
    """
    Search the biggest font size compatible with the width of the GIF. Take the maximum font size if it is lesser than the perfect font size.
    :param image: Image.
    :param font: Path to the font file.
    :param maximum_font_size: Maximum font size.
    :param text: Predicted text.
    :param width: Image width.
    """
    font_size = maximum_font_size
    font_param = None

    # Check for every font size if it's the perfect font size
    while font_param is None:
        loaded_font = load_font(font, font_size)

        if width is not None:
            # Get place taken by the font
            left, _, right, _ = ImageDraw.Draw(image).multiline_textbbox(
                (width, 0), text, loaded_font
            )

            place_taken = right - left
            font_param = loaded_font if place_taken < width else None

        elif height is not None:
            _, top, _, bottom = ImageDraw.Draw(image).multiline_textbbox(
                (width, 0), text, loaded_font
            )

            place_taken = bottom - top
            font_param = loaded_font if place_taken < round(height / 10) else None

        font_size -= 1

        if font_size == 0:
            logger.warn("No compatible font size found")
            break

    return font_param


def search_spacing(
    image: Image,
    font: FreeTypeFont,
    text: str,
    width: int,
    height: int,
) -> int:
    """
    Search the biggest font size compatible with the width of the GIF. Take the maximum font size if it is lesser than the perfect font size.
    :param image: Image.
    :param font: Parameter of the font.
    :param text: Predicted text.
    :param width: Image width.
    :param height: Image height.
    """
    spacing = 50
    searched_spacing = None

    # Check for every font size if it's the perfect font size
    while searched_spacing is None:
        # Get place taken by the font
        _, _, _, bottom = ImageDraw.Draw(image).multiline_textbbox(
            (width, 0), text, font, spacing=spacing
        )

        searched_spacing = spacing if bottom < height else None

        spacing -= 1

        if spacing == 0:
            logger.warn("No compatible spacing found: font size will be set to 1.")
            searched_spacing = 1

    return searched_spacing


def create_image(
    image: Image,
    text: str,
    font: Path,
    maximum_font_size: int,
    contour: ndarray | None = None,
    scale: float | None = None,
    cer: float | None = None,
    wer: float | None = None,
):
    """
    Create an image with predicted text.
    :param image: Image predicted.
    :param text: Text predicted from the image.
    :param font: Path to the font file.
    :param maximum_font_size: Maximum font size to use.
    :param contour: Contour of the predicted text on the image.
    :param scale: Scaling factor for the output image.
    """
    width, height = image.size

    # Double image size so it have a free with space to write
    new_image = Image.new(image.mode, (width * 2, height), (255, 255, 255))
    new_image.paste(image, (0, 0))
    draw = ImageDraw.Draw(new_image)

    # Search the biggest compatible font size
    font_param = search_font_size(new_image, font, maximum_font_size, text, width)

    if font_param is not None and contour is not None:
        contour = (contour * scale).astype(int32)

        # Get the list of every height of every point of the contour
        heights = [coord[0][1] for coord in contour.tolist()]
        average_height = round(mean(heights))
        draw.text((width, average_height), text, (0, 0, 0), font=font_param)

    elif font_param is not None:
        spacing = search_spacing(new_image, font_param, text, width, height)
        draw.text((width, 0), text, (0, 0, 0), font=font_param, spacing=spacing)

    if cer is None or wer is None:
        return new_image

    more_height = round(height / 10)
    new_height = height + more_height
    cer_wer_text = f"CER : {cer}% | WER : {wer}%"

    # Double image size so it have a free with space to write
    result = Image.new(new_image.mode, (width * 2, new_height), (255, 255, 255))
    result.paste(new_image, (0, more_height))

    draw = ImageDraw.Draw(result)
    font_param = search_font_size(result, font, maximum_font_size, cer_wer_text, height)

    _, _, right, top = draw.textbbox((0, 0), cer_wer_text, font=font_param)

    draw.text(
        ((width * 2 - right) / 2, (more_height - top) / 2),
        cer_wer_text,
        (0, 0, 0),
        font=font_param,
    )

    return result
