# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

import shutil

import pytest

from dan.ocr.predict.attention import (
    Level,
    parse_delimiters,
    split_text,
    split_text_and_confidences,
)
from dan.ocr.predict.inference import run as run_prediction
from dan.utils import (
    EntityType,
    parse_charset_pattern,
    parse_tokens,
    parse_tokens_pattern,
)
from tests import FIXTURES

PREDICTION_DATA_PATH = FIXTURES / "prediction"

FONT_PATH = FIXTURES.parent.parent / "fonts/LinuxLibertine.ttf"


@pytest.mark.parametrize(
    (
        "text",
        "confidence",
        "level",
        "tokens",
        "expected_split_text",
        "expected_mean_confidences",
        "expected_offsets",
    ),
    [
        # level: char
        (
            "To <kyo>",
            [0.1, 0.2, 0.3, 0.4],
            Level.Char,
            None,
            ["T", "o", " ", "<kyo>"],
            [0.1, 0.2, 0.3, 0.4],
            [0, 0, 0, 0],
        ),
        # level: word
        (
            "Lo ve\nTokyo",
            [0.1, 0.1, 0.2, 0.3, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5],
            Level.Word,
            None,
            ["Lo", "ve", "Tokyo"],
            [0.1, 0.3, 0.5],
            [1, 1, 0],
        ),
        # level: line
        (
            "Love\nTokyo",
            [0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
            Level.Line,
            None,
            ["Love", "Tokyo"],
            [0.1, 0.3],
            [1, 0],
        ),
        # level: NER (no end tokens)
        (
            "ⒶLove ⒷTokyo",
            [0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5],
            Level.NER,
            [EntityType(start="Ⓐ"), EntityType(start="Ⓑ")],
            ["ⒶLove ", "ⒷTokyo"],
            [0.2, 0.48],
            [0, 0],
        ),
        # level: NER (with end tokens)
        (
            "ⓐLoveⒶ ⓑTokyoⒷ",
            [0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7],
            Level.NER,
            [EntityType(start="ⓐ", end="Ⓐ"), EntityType(start="ⓑ", end="Ⓑ")],
            ["ⓐLoveⒶ", "ⓑTokyoⒷ"],
            [0.2, 0.6],
            [1, 0],
        ),
        # level: NER (no end tokens, no space)
        (
            "ⒶLoveⒷTokyo",
            [0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4],
            Level.NER,
            [EntityType(start="Ⓐ"), EntityType(start="Ⓑ")],
            ["ⒶLove", "ⒷTokyo"],
            [0.18, 0.38],
            [0, 0],
        ),
        # level: NER (with end tokens, no space)
        (
            "ⓐLoveⒶⓑTokyoⒷ",
            [0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6],
            Level.NER,
            [EntityType(start="ⓐ", end="Ⓐ"), EntityType(start="ⓑ", end="Ⓑ")],
            ["ⓐLoveⒶ", "ⓑTokyoⒷ"],
            [0.2, 0.5],
            [0, 0],
        ),
    ],
)
def test_split_text_and_confidences(
    text: str,
    confidence: list[float],
    level: Level,
    tokens: list[EntityType] | None,
    expected_split_text: list[str],
    expected_mean_confidences: list[list[float]],
    expected_offsets: list[int],
):
    # Full charset
    charset = [
        # alphabet
        "T",
        "o",
        "L",
        "v",
        "e",
        "k",
        "y",
        # Entities
        "ⓐ",
        "Ⓐ",
        "ⓑ",
        "Ⓑ",
        # Special
        "<kyo>",
        # Punctuation
        " ",
    ]
    texts_conf, averages_conf, offsets_conf = split_text_and_confidences(
        text=text,
        confidences=confidence,
        level=level,
        char_separators=parse_charset_pattern(charset),
        word_separators=parse_delimiters([" ", "\n"]),
        line_separators=parse_delimiters(["\n"]),
        tokens_separators=parse_tokens_pattern(tokens) if tokens else None,
    )
    texts, offsets = split_text(
        text=text,
        level=level,
        char_separators=parse_charset_pattern(charset),
        word_separators=parse_delimiters([" ", "\n"]),
        line_separators=parse_delimiters(["\n"]),
        tokens_separators=parse_tokens_pattern(tokens) if tokens else None,
    )

    assert texts == expected_split_text
    assert offsets == expected_offsets
    assert texts_conf == expected_split_text
    assert averages_conf == expected_mean_confidences
    assert offsets_conf == expected_offsets


def test_plot_attention(
    tmp_path,
):
    confidence_score = []

    image_name = "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84"

    image_dir = tmp_path / "images"
    image_dir.mkdir()
    shutil.copyfile(
        (PREDICTION_DATA_PATH / "images" / image_name).with_suffix(".png"),
        (image_dir / image_name).with_suffix(".png"),
    )

    run_prediction(
        image_dir=image_dir,
        font=FONT_PATH,
        maximum_font_size=32,
        model=PREDICTION_DATA_PATH,
        output=tmp_path,
        confidence_score=bool(confidence_score),
        confidence_score_levels=confidence_score,
        attention_map=True,
        attention_map_level=[Level.Line].pop(),
        attention_map_scale=0.5,
        alpha_factor=0.9,
        color_map="nipy_spectral",
        word_separators=[" ", "\n"],
        line_separators=["\n"],
        temperature=1.0,
        predict_objects=True,
        max_object_height=None,
        image_extension=".png",
        gpu_device=None,
        batch_size=1,
        tokens=parse_tokens(PREDICTION_DATA_PATH / "tokens.yml"),
        start_token=None,
        use_language_model=False,
        compile_model=False,
        dynamic_mode=False,
    )

    outname = image_name + "_line.gif"

    assert (tmp_path / outname).read_bytes() == (
        PREDICTION_DATA_PATH / outname
    ).read_bytes()
