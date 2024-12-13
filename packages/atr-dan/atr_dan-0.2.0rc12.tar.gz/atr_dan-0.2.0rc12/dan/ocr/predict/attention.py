# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import logging
import re
from enum import Enum
from pathlib import Path
from typing import List, Tuple

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
from torchvision.transforms.functional import to_pil_image

from dan.ocr.utils import create_image

logger = logging.getLogger(__name__)


class Level(str, Enum):
    Char = "char"
    Word = "word"
    Line = "line"
    NER = "ner"

    def __str__(self):
        return self.value


def parse_delimiters(delimiters: List[str]) -> re.Pattern:
    return re.compile(rf"[^{'|'.join(delimiters)}]+")


def compute_offsets_by_level(full_text: str, level: Level, text_list: List[str]):
    """
    Compute and return the list of offset between each text part.
    :param full_text: predicted text.
    :param level: Level to use from [char, word, line, ner].
    :param text_list: list of text to use.
    Returns a list of offsets.
    """
    # offsets[idx] = number of characters between text_list[idx-1] and text_list[idx]
    offsets = [int(level != Level.Char)] * (len(text_list) - 1)
    # Take entities into account if there are any
    if level == Level.NER and text_list:
        # Start after the first entity
        cursor = len(text_list[0])
        for idx, split in enumerate(text_list[1:]):
            # Number of characters between this entity and the previous one
            offsets[idx] = full_text[cursor:].index(split)
            cursor += offsets[idx] + len(split)

    # Last offset is not used, padded with a 0 to match the length of text_list
    return offsets + [0]


def compute_prob_by_separator(
    characters: str, probabilities: List[float], separator: re.Pattern
) -> Tuple[List[str], List[np.float64]]:
    """
    Split text and confidences using separators and return a list of average confidence scores.
    :param characters: list of characters.
    :param probabilities: list of character probabilities.
    :param separators: regex for separators. Use parse_delimiters(["\n", " "]) for word confidences and parse_delimiters(["\n"]) for line confidences.
    Returns a list confidence scores.
    """
    # match anything except separators, get start and end index
    matches = [(m.start(), m.end()) for m in separator.finditer(characters)]

    # Iterate over text pieces and compute mean confidence
    return [characters[start:end] for (start, end) in matches], [
        np.mean(probabilities[start:end]) for (start, end) in matches
    ]


def split_text(
    text: str,
    level: Level,
    char_separators: re.Pattern,
    word_separators: re.Pattern,
    line_separators: re.Pattern,
    tokens_separators: re.Pattern | None = None,
) -> Tuple[List[str], List[int]]:
    """
    Split text into a list of characters, word, or lines.
    :param text: Text prediction from DAN
    :param level: Level to visualize from [char, word, line, ner]
    :param char_separators: Pattern used to find tokens in the charset
    :param word_separators: Pattern used to find words
    :param line_separators: Pattern used to find lines
    :param tokens_separators: Pattern used to find NER entities
    """
    match level:
        case Level.Char:
            text_split = char_separators.findall(text)
        # split into words
        case Level.Word:
            text_split = word_separators.findall(text)
        # split into lines
        case Level.Line:
            text_split = line_separators.findall(text)
        # split into entities
        case Level.NER:
            if not tokens_separators:
                logger.error("Cannot compute NER level: tokens not found")
                return [], []
            matches = [(m.start(), m.end()) for m in tokens_separators.finditer(text)]
            text_split = [text[start:end] for (start, end) in matches]
        case _:
            logger.error(f"Level should be either {list(map(str, Level))}")
            return [], []
    return text_split, compute_offsets_by_level(text, level, text_split)


def split_text_and_confidences(
    text: str,
    confidences: List[float],
    level: Level,
    char_separators: re.Pattern,
    word_separators: re.Pattern,
    line_separators: re.Pattern,
    tokens_separators: re.Pattern | None = None,
) -> Tuple[List[str], List[np.float64], List[int]]:
    """
    Split text into a list of characters, words or lines with corresponding confidences scores
    :param text: Text prediction from DAN
    :param confidences: Character confidences
    :param level: Level to visualize from [char, word, line, ner]
    :param char_separators: Pattern used to find tokens of the charset
    :param word_separators: Pattern used to find words
    :param line_separators: Pattern used to find lines
    :param tokens_separators: Pattern used to find NER entities
    """
    match level:
        case Level.Char:
            texts = char_separators.findall(text)
        case Level.Word:
            texts, confidences = compute_prob_by_separator(
                text, confidences, word_separators
            )
        case Level.Line:
            texts, confidences = compute_prob_by_separator(
                text, confidences, line_separators
            )
        case Level.NER:
            if not tokens_separators:
                logger.error("Cannot compute NER level: tokens not found")
                return [], [], []

            texts, confidences = compute_prob_by_separator(
                text, confidences, tokens_separators
            )
        case _:
            logger.error(f"Level should be either {list(map(str, Level))}")
            return [], [], []
    return (
        texts,
        [np.around(num, 2) for num in confidences],
        compute_offsets_by_level(text, level, texts),
    )


def get_predicted_polygons_with_confidence(
    text: str,
    weights: np.ndarray,
    confidences: List[float],
    level: Level,
    height: int,
    width: int,
    char_separators: re.Pattern,
    max_object_height: int = 50,
    word_separators: re.Pattern = parse_delimiters(["\n", " "]),
    line_separators: re.Pattern = parse_delimiters(["\n"]),
    tokens_separators: re.Pattern | None = None,
) -> List[dict]:
    """
    Returns the polygons of each object of the current prediction
    :param text: Text predicted by DAN
    :param weights: Attention weights of size (n_char, feature_height, feature_width)
    :param confidences: Character confidences
    :param level: Level to display (must be in [char, word, line, ner])
    :param height: Original image height
    :param width: Original image width
    :param char_separators: Pattern used to find tokens of the charset
    :param max_object_height: Maximum height of predicted objects.
    :param word_separators: Pattern used to find words
    :param line_separators: Pattern used to find lines
    :param tokens_separators: Pattern used to find NER entities
    """
    # Split text into characters, words or lines
    text_list, confidence_list, offsets = split_text_and_confidences(
        text,
        confidences,
        level,
        char_separators,
        word_separators,
        line_separators,
        tokens_separators,
    )

    max_value = weights.sum(0).max()
    polygons = []
    start_index = 0
    for text_piece, confidence, offset in zip(text_list, confidence_list, offsets):
        polygon, _ = get_polygon(
            text_piece,
            max_value,
            start_index,
            weights,
            max_object_height=max_object_height,
            size=(width, height),
        )
        start_index += len(text_piece) + offset
        if not polygon:
            continue
        polygon["text"] = text_piece
        polygon["text_confidence"] = confidence
        polygons.append(polygon)
    return polygons


def compute_coverage(
    text: str,
    max_value: np.float32,
    offset: int,
    attentions: np.ndarray,
    size: Tuple[int, int],
) -> np.ndarray:
    """
    Aggregates attention maps for the current text piece (char, word, line)
    :param text: Text piece selected with offset after splitting DAN prediction
    :param max_value: Maximum "attention intensity" for parts of a text piece, used for normalization
    :param offset: Offset value to get the relevant part of text piece
    :param attentions: Attention weights of size (n_char, feature_height, feature_width)
    :param size: Target size (width, height) to resize the coverage vector
    """
    _, height, width = attentions.shape

    # blank vector to accumulate weights for the current text
    coverage_vector = np.zeros((height, width))
    for i in range(len(text)):
        local_weight = cv2.resize(attentions[i + offset], (width, height))
        coverage_vector = np.clip(coverage_vector + local_weight, 0, 1)

    # Normalize coverage vector
    coverage_vector = (coverage_vector / max_value * 255).astype(np.uint8)

    # Resize it
    if size:
        coverage_vector = cv2.resize(coverage_vector, size)

    return coverage_vector


def blend_coverage(
    coverage_vector: np.ndarray,
    image: Image.Image,
    scale: float,
    alpha_factor: float,
    color_map: str,
) -> Image.Image:
    """
    Blends current coverage_vector over original image, used to make an attention map.
    :param coverage_vector: Aggregated attention weights of the current text piece, resized to image. size: (n_char, image_height, image_width)
    :param image: Input image in PIL format
    :param scale: Scaling factor for the output gif image
    :param alpha_factor: Alpha factor that controls how much the attention map is shown to the user during prediction. (higher value means more transparency for the attention map, commonly between 0.5 and 1.0)
    :param color_map: Colormap to use for the attention map (from matplotlib colormaps)
    """
    height, width = coverage_vector.shape

    # Make a colormap so colors are can be applied based on a scale
    cmap = plt.get_cmap(color_map)

    # Normalize the coverage_vector to the range [0, 255]
    norm = plt.Normalize(vmin=0, vmax=255)

    # Apply the colormap to the normalized coverage_vector to get color values
    color = cmap(norm(coverage_vector))

    # Get a transparency map from the coverage_vector with a power function
    # higher alpha_factor means more transparency of the attention map
    #  with 1 as no change (commonly between 0.5 and 1.0)
    alpha = (coverage_vector / 255.0) ** alpha_factor

    # Add the alpha channel to the color map
    color = np.dstack((color[:, :, :3], alpha))

    # Convert the color map to a RGBA image and all channels to a 0-255 range (as all values are between 0 and 1)
    color = Image.fromarray((color * 255).astype(np.uint8), "RGBA")

    # Convert the original image to RGBA
    image = image.convert("RGBA")

    # Blend the two images together so the original image shows through the attention map
    blend = Image.alpha_composite(image, color)

    # Resize the image to the desired scale in order to reduce the time need to create the gif
    blend = blend.resize((int(width * scale), int(height * scale)), Image.LANCZOS)

    return blend


def compute_contour_metrics(
    coverage_vector: np.ndarray, contour: np.ndarray
) -> Tuple[np.float64, np.float64]:
    """
    Compute the contours's area and the mean value inside it.
    :param coverage_vector: Aggregated attention weights of the current text piece, resized to image. size: (n_char, image_height, image_width)
    :param contour: Contour of the current attention blob
    """
    # draw the contour zone
    mask = np.zeros(coverage_vector.shape, dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, (255), -1)

    max_value = np.where(mask > 0, coverage_vector, 0).max() / 255
    area = cv2.contourArea(contour)
    return max_value, max_value * area


def polygon_to_bbx(polygon: np.ndarray) -> List[Tuple[int, int]]:
    x, y, w, h = cv2.boundingRect(polygon)
    return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]


def threshold(mask: np.ndarray) -> np.ndarray:
    """
    Threshold a grayscale mask.
    :param mask: a grayscale image (np.array)
    """
    min_kernel = 1
    max_kernel = mask.shape[1] // 100

    # Blur and apply Otsu thresholding
    blur = cv2.GaussianBlur(mask, (15, 15), 0)
    _, bin_mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Apply dilation
    kernel_width = cv2.getStructuringElement(cv2.MORPH_CROSS, (max_kernel, min_kernel))
    dilated = cv2.dilate(bin_mask, kernel_width, iterations=3)
    return np.asarray(dilated, dtype=np.uint8)


def get_polygon(
    text: str,
    max_value: np.float32,
    offset: int,
    weights: np.ndarray,
    size: Tuple[int, int] | None = None,
    max_object_height: int = 50,
) -> Tuple[dict, np.ndarray | None]:
    """
    Gets polygon associated with element of current text_piece, indexed by offset
    :param text: Text piece selected with offset after splitting DAN prediction
    :param max_value: Maximum "attention intensity" for parts of a text piece, used for normalization
    :param offset: Offset value to get the relevant part of text piece
    :param size: Target size (width, height) to resize the coverage vector
    :param max_object_height: Maximum height of predicted objects.
    """
    # Compute coverage vector
    coverage_vector = compute_coverage(text, max_value, offset, weights, size=size)

    # Generate a binary image for the current channel.
    bin_mask = threshold(coverage_vector)

    coord, confidence = (
        get_grid_search_contour(coverage_vector, bin_mask, height=max_object_height)
        if max_object_height
        else get_best_contour(coverage_vector, bin_mask)
    )
    if not coord or confidence is None:
        return {}, None

    # Format for JSON
    polygon = {
        "confidence": confidence,
        "polygon": coord,
    }
    simplified_contour = np.expand_dims(np.array(coord, dtype=np.int32), axis=1)

    return polygon, simplified_contour


def get_best_contour(coverage_vector, bin_mask):
    """
    Detect the objects contours using opencv and select the best one.
    """
    contours, _ = cv2.findContours(bin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return [], None

    # Select best contour
    metrics = [compute_contour_metrics(coverage_vector, cnt) for cnt in contours]
    confidences, scores = map(list, zip(*metrics))
    best_contour = contours[np.argmax(scores)]
    coord = polygon_to_bbx(np.squeeze(best_contour))
    confidence = round(confidences[np.argmax(scores)], 2)
    return coord, confidence


def get_grid_search_contour(coverage_vector, bin_mask, height=50):
    """
    Perform grid search to find the best contour with fixed width and height.
    """
    # Limit search area based on attention values
    roi = np.argwhere(bin_mask == 255)

    if not np.any(roi):
        return [], None

    y_min, y_max = roi[:, 0].min(), roi[:, 0].max()

    # Limit bounding box shape
    width = bin_mask.shape[1]

    best_sum_att = 0
    for y in range(y_min, max(y_max - height, y_min + 1)):
        sum_att = coverage_vector[y : y + height, 0:width].sum()
        if sum_att > best_sum_att:
            best_sum_att = sum_att
            best_coordinates = [0, y, width, height]
            confidence = coverage_vector[y : y + height, 0:width].max()

    # Format for JSON
    x, y, w, h = best_coordinates
    coord = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
    confidence = round(confidence / 255.0, 2)
    return coord, confidence


def plot_attention(
    image: torch.Tensor,
    text: str,
    weights: np.ndarray,
    level: Level,
    scale: float,
    outname: str,
    alpha_factor: float,
    color_map: str,
    char_separators: re.Pattern,
    font: Path,
    maximum_font_size: int,
    max_object_height: int = 50,
    word_separators: re.Pattern = parse_delimiters(["\n", " "]),
    line_separators: re.Pattern = parse_delimiters(["\n"]),
    tokens_separators: re.Pattern | None = None,
    display_polygons: bool = False,
) -> None:
    """
    Create a gif by blending attention maps to the image for each text piece (char, word or line)
    :param image: Input image as torch.Tensor
    :param text: Text predicted by DAN
    :param weights: Attention weights of size (n_char, feature_height, feature_width)
    :param level: Level to display (must be in [char, word, line, ner])
    :param scale: Scaling factor for the output gif image
    :param outname: Name of the gif image
    :param alpha_factor: Alpha factor that controls how much the attention map is shown to the user during prediction. (higher value means more transparency for the attention map, commonly between 0.5 and 1.0)
    :param color_map: Colormap to use for the attention map
    :param char_separators: Pattern used to find tokens of the charset
    :param font : Path to the font file to use for the GIF of the attention map.
    :param maximum_font_size: Maximum font size to use for the GIF of the attention map. Default is 32.
    :param max_object_height: Maximum height of predicted objects.
    :param word_separators: Pattern used to find words
    :param line_separators: Pattern used to find lines
    :param tokens_separators: Pattern used to find NER entities
    :param display_polygons: Whether to plot extracted polygons
    """
    image = to_pil_image(image)
    attention_map = []

    # Split text into characters, words or lines
    text_list, offsets = split_text(
        text,
        level,
        char_separators,
        word_separators,
        line_separators,
        tokens_separators,
    )

    # Iterate on characters, words or lines
    tot_len = 0
    max_value = weights.sum(0).max()

    for text_piece, offset in zip(text_list, offsets):
        # Accumulate weights for the current word/line and resize to original image size
        coverage_vector = compute_coverage(
            text_piece, max_value, tot_len, weights, (image.width, image.height)
        )

        # Blend coverage vector with original image to make an attention map
        blended = blend_coverage(coverage_vector, image, scale, alpha_factor, color_map)

        # Draw the contour
        polygon, contour = get_polygon(
            text_piece,
            max_value,
            tot_len,
            weights,
            max_object_height=max_object_height,
            size=(image.width, image.height),
        )

        if contour is not None:
            blended = create_image(
                blended, text_piece, font, maximum_font_size, contour, scale
            )

            contour = (contour * scale).astype(np.int32)

            if display_polygons:
                # Draw the contour with a thickness based on the scale in red
                cv2.drawContours(
                    blended := np.array(blended),
                    [contour],
                    0,
                    (255, 0, 0, 1),
                    int(5 * scale),
                )

                # Make the np.array with drawn contours back into a PIL image
                blended = Image.fromarray(blended, "RGBA")

        # Keep track of text length
        tot_len += len(text_piece) + offset

        # Append the blended image to the list of attention maps to be used for the .gif
        attention_map.append(blended)

    if not attention_map:
        return

    attention_map[0].save(
        outname,
        save_all=True,
        format="GIF",
        append_images=attention_map[1:],
        duration=1000,
        loop=True,
    )
