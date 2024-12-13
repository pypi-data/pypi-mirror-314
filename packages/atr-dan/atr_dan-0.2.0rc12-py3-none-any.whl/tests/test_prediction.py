# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import json
import shutil
from pathlib import Path

import numpy as np
import pytest
import yaml

from dan.ocr.predict.attention import Level
from dan.ocr.predict.inference import DAN
from dan.ocr.predict.inference import run as run_prediction
from dan.utils import (
    parse_charset_pattern,
    parse_tokens,
    read_yaml,
)
from tests import FIXTURES

PREDICTION_DATA_PATH = FIXTURES / "prediction"

FONT_PATH = FIXTURES.parent.parent / "fonts/LinuxLibertine.ttf"
MAXIMUM_FONT_SIZE = 32


@pytest.mark.parametrize(
    "image_name, expected_prediction",
    (
        (
            "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84.png",
            {"text": ["ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241"]},
        ),
        (
            "0dfe8bcd-ed0b-453e-bf19-cc697012296e.png",
            {"text": ["ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376"]},
        ),
        (
            "2c242f5c-e979-43c4-b6f2-a6d4815b651d.png",
            {"text": ["Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31"]},
        ),
        (
            "ffdec445-7f14-4f5f-be44-68d0844d0df1.png",
            {"text": ["ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère"]},
        ),
    ),
)
@pytest.mark.parametrize("normalize", (True, False))
def test_predict(image_name, expected_prediction, normalize, tmp_path):
    # Update mean/std in parameters.yml
    model_path = tmp_path / "models"
    model_path.mkdir(exist_ok=True)

    shutil.copyfile(
        PREDICTION_DATA_PATH / "model.pt",
        model_path / "model.pt",
    )
    shutil.copyfile(
        PREDICTION_DATA_PATH / "charset.pkl",
        model_path / "charset.pkl",
    )

    params = read_yaml(PREDICTION_DATA_PATH / "parameters.yml")
    if not normalize:
        del params["parameters"]["mean"]
        del params["parameters"]["std"]
    yaml.dump(params, (model_path / "parameters.yml").open("w"))

    device = "cpu"

    dan_model = DAN(device)
    dan_model.load(path=model_path, mode="eval")

    image_path = PREDICTION_DATA_PATH / "images" / image_name
    _, image = dan_model.preprocess(str(image_path))

    input_tensor = image.unsqueeze(0)
    input_tensor = input_tensor.to(device)
    input_sizes = [image.shape[1:]]

    prediction = dan_model.predict(
        input_tensor,
        input_sizes,
        char_separators=parse_charset_pattern(dan_model.charset),
    )

    assert prediction == expected_prediction


@pytest.mark.parametrize(
    "image_name, confidence_score, temperature, predict_objects, expected_prediction",
    (
        (
            "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
            [],  # Confidence score
            1.0,  # Temperature
            False,  # Predict objects
            {
                "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                "language_model": {},
                "confidences": {},
            },
        ),
        (
            "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
            [Level.Word],  # Confidence score
            1.0,  # Temperature
            True,  # Predict objects
            {
                "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                "language_model": {},
                "confidences": {
                    "total": 1.0,
                    "word": [
                        {"text": "ⓈBellisson", "confidence": 1.0},
                        {"text": "ⒻGeorges", "confidence": 1.0},
                        {"text": "Ⓑ91", "confidence": 1.0},
                        {"text": "ⓁP", "confidence": 1.0},
                        {"text": "ⒸM", "confidence": 1.0},
                        {"text": "ⓀCh", "confidence": 1.0},
                        {"text": "ⓄPlombier", "confidence": 1.0},
                        {"text": "ⓅPatron?12241", "confidence": 1.0},
                    ],
                },
                "objects": [
                    {
                        "confidence": 0.42,
                        "polygon": [[0, 0], [144, 0], [144, 66], [0, 66]],
                        "text": "ⓈBellisson",
                        "text_confidence": 1.0,
                    },
                    {
                        "confidence": 0.52,
                        "polygon": [[184, 0], [269, 0], [269, 66], [184, 66]],
                        "text": "ⒻGeorges",
                        "text_confidence": 1.0,
                    },
                    {
                        "confidence": 0.21,
                        "polygon": [[294, 0], [371, 0], [371, 66], [294, 66]],
                        "text": "Ⓑ91",
                        "text_confidence": 1.0,
                    },
                    {
                        "confidence": 0.23,
                        "polygon": [[367, 0], [427, 0], [427, 66], [367, 66]],
                        "text": "ⓁP",
                        "text_confidence": 1.0,
                    },
                    {
                        "confidence": 0.18,
                        "polygon": [[535, 0], [619, 0], [619, 66], [535, 66]],
                        "text": "ⒸM",
                        "text_confidence": 1.0,
                    },
                    {
                        "confidence": 0.23,
                        "polygon": [[589, 0], [674, 0], [674, 66], [589, 66]],
                        "text": "ⓀCh",
                        "text_confidence": 1.0,
                    },
                    {
                        "confidence": 0.31,
                        "polygon": [[685, 0], [806, 0], [806, 66], [685, 66]],
                        "text": "ⓄPlombier",
                        "text_confidence": 1.0,
                    },
                    {
                        "confidence": 0.91,
                        "polygon": [[820, 0], [938, 0], [938, 66], [820, 66]],
                        "text": "ⓅPatron?12241",
                        "text_confidence": 1.0,
                    },
                ],
                "attention_gif": "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84_word.gif",
            },
        ),
        (
            "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
            [Level.NER, Level.Word],  # Confidence score
            3.5,  # Temperature
            False,  # Predict objects
            {
                "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                "language_model": {},
                "confidences": {
                    "total": 0.93,
                    "ner": [
                        {"text": "ⓈBellisson ", "confidence": 0.92},
                        {"text": "ⒻGeorges ", "confidence": 0.94},
                        {"text": "Ⓑ91 ", "confidence": 0.93},
                        {"text": "ⓁP ", "confidence": 0.92},
                        {"text": "ⒸM ", "confidence": 0.93},
                        {"text": "ⓀCh ", "confidence": 0.95},
                        {"text": "ⓄPlombier ", "confidence": 0.93},
                        {"text": "ⓅPatron?12241", "confidence": 0.93},
                    ],
                    "word": [
                        {"text": "ⓈBellisson", "confidence": 0.93},
                        {"text": "ⒻGeorges", "confidence": 0.94},
                        {"text": "Ⓑ91", "confidence": 0.92},
                        {"text": "ⓁP", "confidence": 0.94},
                        {"text": "ⒸM", "confidence": 0.93},
                        {"text": "ⓀCh", "confidence": 0.96},
                        {"text": "ⓄPlombier", "confidence": 0.94},
                        {"text": "ⓅPatron?12241", "confidence": 0.93},
                    ],
                },
            },
        ),
        (
            "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
            [Level.Line],  # Confidence score
            1.0,  # Temperature
            False,  # Predict objects
            {
                "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                "language_model": {},
                "confidences": {
                    "total": 1.0,
                    "line": [
                        {
                            "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                            "confidence": 1.0,
                        }
                    ],
                },
            },
        ),
        (
            "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
            [Level.NER, Level.Line],  # Confidence score
            3.5,  # Temperature
            False,  # Predict objects
            {
                "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                "language_model": {},
                "confidences": {
                    "total": 0.93,
                    "ner": [
                        {"text": "ⓈBellisson ", "confidence": 0.92},
                        {"text": "ⒻGeorges ", "confidence": 0.94},
                        {"text": "Ⓑ91 ", "confidence": 0.93},
                        {"text": "ⓁP ", "confidence": 0.92},
                        {"text": "ⒸM ", "confidence": 0.93},
                        {"text": "ⓀCh ", "confidence": 0.95},
                        {"text": "ⓄPlombier ", "confidence": 0.93},
                        {"text": "ⓅPatron?12241", "confidence": 0.93},
                    ],
                    "line": [
                        {
                            "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                            "confidence": 0.93,
                        }
                    ],
                },
            },
        ),
        (
            "0dfe8bcd-ed0b-453e-bf19-cc697012296e",
            [],  # Confidence score
            1.0,  # Temperature
            False,  # Predict objects
            {
                "text": "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",
                "language_model": {},
                "confidences": {},
            },
        ),
        (
            "0dfe8bcd-ed0b-453e-bf19-cc697012296e",
            [Level.NER, Level.Char, Level.Word, Level.Line],  # Confidence score
            1.0,  # Temperature
            False,  # Predict objects
            {
                "text": "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",
                "language_model": {},
                "confidences": {
                    "total": 1.0,
                    "ner": [
                        {"text": "ⓈTemplié ", "confidence": 0.98},
                        {"text": "ⒻMarcelle ", "confidence": 1.0},
                        {"text": "Ⓑ93 ", "confidence": 1.0},
                        {"text": "ⓁS ", "confidence": 1.0},
                        {"text": "Ⓚch ", "confidence": 1.0},
                        {"text": "ⓄE dactylo ", "confidence": 1.0},
                        {"text": "Ⓟ18376", "confidence": 1.0},
                    ],
                    "char": [
                        {"text": "Ⓢ", "confidence": 1.0},
                        {"text": "T", "confidence": 1.0},
                        {"text": "e", "confidence": 1.0},
                        {"text": "m", "confidence": 1.0},
                        {"text": "p", "confidence": 1.0},
                        {"text": "l", "confidence": 1.0},
                        {"text": "i", "confidence": 1.0},
                        {"text": "é", "confidence": 0.85},
                        {"text": " ", "confidence": 1.0},
                        {"text": "Ⓕ", "confidence": 1.0},
                        {"text": "M", "confidence": 1.0},
                        {"text": "a", "confidence": 1.0},
                        {"text": "r", "confidence": 1.0},
                        {"text": "c", "confidence": 1.0},
                        {"text": "e", "confidence": 1.0},
                        {"text": "l", "confidence": 1.0},
                        {"text": "l", "confidence": 1.0},
                        {"text": "e", "confidence": 1.0},
                        {"text": " ", "confidence": 1.0},
                        {"text": "Ⓑ", "confidence": 1.0},
                        {"text": "9", "confidence": 1.0},
                        {"text": "3", "confidence": 1.0},
                        {"text": " ", "confidence": 1.0},
                        {"text": "Ⓛ", "confidence": 1.0},
                        {"text": "S", "confidence": 1.0},
                        {"text": " ", "confidence": 1.0},
                        {"text": "Ⓚ", "confidence": 1.0},
                        {"text": "c", "confidence": 1.0},
                        {"text": "h", "confidence": 1.0},
                        {"text": " ", "confidence": 1.0},
                        {"text": "Ⓞ", "confidence": 1.0},
                        {"text": "E", "confidence": 1.0},
                        {"text": " ", "confidence": 1.0},
                        {"text": "d", "confidence": 1.0},
                        {"text": "a", "confidence": 1.0},
                        {"text": "c", "confidence": 1.0},
                        {"text": "t", "confidence": 1.0},
                        {"text": "y", "confidence": 1.0},
                        {"text": "l", "confidence": 1.0},
                        {"text": "o", "confidence": 1.0},
                        {"text": " ", "confidence": 1.0},
                        {"text": "Ⓟ", "confidence": 1.0},
                        {"text": "1", "confidence": 1.0},
                        {"text": "8", "confidence": 1.0},
                        {"text": "3", "confidence": 1.0},
                        {"text": "7", "confidence": 1.0},
                        {"text": "6", "confidence": 1.0},
                    ],
                    "word": [
                        {"text": "ⓈTemplié", "confidence": 0.98},
                        {"text": "ⒻMarcelle", "confidence": 1.0},
                        {"text": "Ⓑ93", "confidence": 1.0},
                        {"text": "ⓁS", "confidence": 1.0},
                        {"text": "Ⓚch", "confidence": 1.0},
                        {"text": "ⓄE", "confidence": 1.0},
                        {"text": "dactylo", "confidence": 1.0},
                        {"text": "Ⓟ18376", "confidence": 1.0},
                    ],
                    "line": [
                        {
                            "text": "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",
                            "confidence": 1.0,
                        }
                    ],
                },
            },
        ),
        (
            "2c242f5c-e979-43c4-b6f2-a6d4815b651d",
            [],  # Confidence score
            1.0,  # Temperature
            False,  # Predict objects
            {
                "text": "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31",
                "language_model": {},
                "confidences": {},
            },
        ),
        (
            "ffdec445-7f14-4f5f-be44-68d0844d0df1",
            [],  # Confidence score
            1.0,  # Temperature
            True,  # Predict objects
            {
                "text": "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",
                "language_model": {},
                "confidences": {},
                "objects": [
                    {
                        "confidence": 0.96,
                        "polygon": [[546, 0], [715, 0], [715, 67], [546, 67]],
                        "text": "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",
                        "text_confidence": 1.0,
                    }
                ],
            },
        ),
    ),
)
def test_run_prediction(
    image_name,
    confidence_score,
    temperature,
    predict_objects,
    expected_prediction,
    tmp_path,
):
    if "attention_gif" in expected_prediction:
        expected_prediction["attention_gif"] = str(
            tmp_path / expected_prediction["attention_gif"]
        )

    # Make tmpdir and copy needed image inside
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    shutil.copyfile(
        (PREDICTION_DATA_PATH / "images" / image_name).with_suffix(".png"),
        (image_dir / image_name).with_suffix(".png"),
    )

    run_prediction(
        image_dir=image_dir,
        font=FONT_PATH,
        maximum_font_size=MAXIMUM_FONT_SIZE,
        model=PREDICTION_DATA_PATH,
        output=tmp_path,
        confidence_score=bool(confidence_score),
        confidence_score_levels=confidence_score,
        attention_map=predict_objects and confidence_score,
        attention_map_level=[Level.Line, *confidence_score].pop(),
        attention_map_scale=0.5,
        alpha_factor=0.9,
        color_map="nipy_spectral",
        word_separators=[" ", "\n"],
        line_separators=["\n"],
        temperature=temperature,
        predict_objects=predict_objects,
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

    prediction = json.loads((tmp_path / image_name).with_suffix(".json").read_text())
    assert prediction == expected_prediction
    if "attention_gif" in expected_prediction:
        assert Path(expected_prediction["attention_gif"]).exists()


@pytest.mark.parametrize(
    "image_names, confidence_score, temperature, expected_predictions",
    (
        (
            ["0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84"],
            None,
            1.0,
            [
                {
                    "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    "language_model": {},
                    "confidences": {},
                }
            ],
        ),
        (
            ["0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84"],
            [Level.Word],
            1.0,
            [
                {
                    "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    "language_model": {},
                    "confidences": {
                        "total": 1.0,
                        "word": [
                            {"text": "ⓈBellisson", "confidence": 1.0},
                            {"text": "ⒻGeorges", "confidence": 1.0},
                            {"text": "Ⓑ91", "confidence": 1.0},
                            {"text": "ⓁP", "confidence": 1.0},
                            {"text": "ⒸM", "confidence": 1.0},
                            {"text": "ⓀCh", "confidence": 1.0},
                            {"text": "ⓄPlombier", "confidence": 1.0},
                            {"text": "ⓅPatron?12241", "confidence": 1.0},
                        ],
                    },
                }
            ],
        ),
        (
            [
                "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
                "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
            ],
            [Level.NER, Level.Word],
            1.0,
            [
                {
                    "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    "language_model": {},
                    "confidences": {
                        "total": 1.0,
                        "ner": [
                            {"text": "ⓈBellisson ", "confidence": 1.0},
                            {"text": "ⒻGeorges ", "confidence": 1.0},
                            {"text": "Ⓑ91 ", "confidence": 1.0},
                            {"text": "ⓁP ", "confidence": 1.0},
                            {"text": "ⒸM ", "confidence": 1.0},
                            {"text": "ⓀCh ", "confidence": 1.0},
                            {"text": "ⓄPlombier ", "confidence": 1.0},
                            {"text": "ⓅPatron?12241", "confidence": 1.0},
                        ],
                        "word": [
                            {"text": "ⓈBellisson", "confidence": 1.0},
                            {"text": "ⒻGeorges", "confidence": 1.0},
                            {"text": "Ⓑ91", "confidence": 1.0},
                            {"text": "ⓁP", "confidence": 1.0},
                            {"text": "ⒸM", "confidence": 1.0},
                            {"text": "ⓀCh", "confidence": 1.0},
                            {"text": "ⓄPlombier", "confidence": 1.0},
                            {"text": "ⓅPatron?12241", "confidence": 1.0},
                        ],
                    },
                },
                {
                    "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    "language_model": {},
                    "confidences": {
                        "total": 1.0,
                        "ner": [
                            {"text": "ⓈBellisson ", "confidence": 1.0},
                            {"text": "ⒻGeorges ", "confidence": 1.0},
                            {"text": "Ⓑ91 ", "confidence": 1.0},
                            {"text": "ⓁP ", "confidence": 1.0},
                            {"text": "ⒸM ", "confidence": 1.0},
                            {"text": "ⓀCh ", "confidence": 1.0},
                            {"text": "ⓄPlombier ", "confidence": 1.0},
                            {"text": "ⓅPatron?12241", "confidence": 1.0},
                        ],
                        "word": [
                            {"text": "ⓈBellisson", "confidence": 1.0},
                            {"text": "ⒻGeorges", "confidence": 1.0},
                            {"text": "Ⓑ91", "confidence": 1.0},
                            {"text": "ⓁP", "confidence": 1.0},
                            {"text": "ⒸM", "confidence": 1.0},
                            {"text": "ⓀCh", "confidence": 1.0},
                            {"text": "ⓄPlombier", "confidence": 1.0},
                            {"text": "ⓅPatron?12241", "confidence": 1.0},
                        ],
                    },
                },
            ],
        ),
        (
            ["0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84"],
            [Level.Word],
            1.0,
            [
                {
                    "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    "language_model": {},
                    "confidences": {
                        "total": 1.0,
                        "word": [
                            {"text": "ⓈBellisson", "confidence": 1.0},
                            {"text": "ⒻGeorges", "confidence": 1.0},
                            {"text": "Ⓑ91", "confidence": 1.0},
                            {"text": "ⓁP", "confidence": 1.0},
                            {"text": "ⒸM", "confidence": 1.0},
                            {"text": "ⓀCh", "confidence": 1.0},
                            {"text": "ⓄPlombier", "confidence": 1.0},
                            {"text": "ⓅPatron?12241", "confidence": 1.0},
                        ],
                    },
                }
            ],
        ),
        (
            [
                "2c242f5c-e979-43c4-b6f2-a6d4815b651d",
                "ffdec445-7f14-4f5f-be44-68d0844d0df1",
            ],
            False,
            1.0,
            [
                {
                    "text": "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31",
                    "language_model": {},
                    "confidences": {},
                },
                {
                    "text": "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",
                    "language_model": {},
                    "confidences": {},
                },
            ],
        ),
    ),
)
@pytest.mark.parametrize("batch_size", [1, 2])
def test_run_prediction_batch(
    image_names,
    confidence_score,
    temperature,
    expected_predictions,
    batch_size,
    tmp_path,
):
    # Make tmpdir and copy needed images inside
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    for image_name in image_names:
        shutil.copyfile(
            (PREDICTION_DATA_PATH / "images" / image_name).with_suffix(".png"),
            (image_dir / image_name).with_suffix(".png"),
        )

    run_prediction(
        image_dir=image_dir,
        font=FONT_PATH,
        maximum_font_size=MAXIMUM_FONT_SIZE,
        model=PREDICTION_DATA_PATH,
        output=tmp_path,
        confidence_score=True if confidence_score else False,
        confidence_score_levels=confidence_score if confidence_score else [],
        attention_map=False,
        attention_map_level=None,
        attention_map_scale=0.5,
        alpha_factor=0.9,
        color_map="nipy_spectral",
        word_separators=[" ", "\n"],
        line_separators=["\n"],
        temperature=temperature,
        predict_objects=False,
        max_object_height=None,
        image_extension=".png",
        gpu_device=None,
        batch_size=batch_size,
        tokens=parse_tokens(PREDICTION_DATA_PATH / "tokens.yml"),
        start_token=None,
        use_language_model=False,
        compile_model=False,
        dynamic_mode=False,
    )

    for image_name, expected_prediction in zip(image_names, expected_predictions):
        prediction = json.loads(
            (tmp_path / image_name).with_suffix(".json").read_text()
        )
        assert prediction == expected_prediction


@pytest.mark.parametrize(
    "image_names, language_model_weight, expected_predictions",
    (
        (
            [
                "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
                "0dfe8bcd-ed0b-453e-bf19-cc697012296e",
                "2c242f5c-e979-43c4-b6f2-a6d4815b651d",
                "ffdec445-7f14-4f5f-be44-68d0844d0df1",
            ],
            1.0,
            [
                {
                    "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    "language_model": {
                        "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                        "confidence": 0.92,
                    },
                },
                {
                    "text": "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",
                    "language_model": {
                        "text": "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",
                        "confidence": 0.88,
                    },
                },
                {
                    "text": "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31",
                    "language_model": {
                        "text": "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31",
                        "confidence": 0.86,
                    },
                },
                {
                    "text": "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",
                    "language_model": {
                        "text": "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",
                        "confidence": 0.89,
                    },
                },
            ],
        ),
        (
            [
                "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
                "0dfe8bcd-ed0b-453e-bf19-cc697012296e",
                "2c242f5c-e979-43c4-b6f2-a6d4815b651d",
                "ffdec445-7f14-4f5f-be44-68d0844d0df1",
            ],
            2.0,
            [
                {
                    "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    "language_model": {
                        "text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                        "confidence": 0.90,
                    },
                },
                {
                    "text": "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",
                    "language_model": {
                        "text": "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",
                        "confidence": 0.84,
                    },
                },
                {
                    "text": "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31",
                    "language_model": {
                        "text": "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14331",
                        "confidence": 0.83,
                    },
                },
                {
                    "text": "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",
                    "language_model": {
                        "text": "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",
                        "confidence": 0.86,
                    },
                },
            ],
        ),
        (
            [
                "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84",
                "0dfe8bcd-ed0b-453e-bf19-cc697012296e",
                "2c242f5c-e979-43c4-b6f2-a6d4815b651d",
                "ffdec445-7f14-4f5f-be44-68d0844d0df1",
            ],
            0.0,
            [
                {"text": "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241"},
                {"text": "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376"},
                {"text": "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31"},
                {"text": "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère"},
            ],
        ),
    ),
)
def test_run_prediction_language_model(
    image_names,
    language_model_weight,
    expected_predictions,
    tmp_path,
):
    # Make tmpdir and copy needed images inside
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    for image_name in image_names:
        shutil.copyfile(
            (PREDICTION_DATA_PATH / "images" / image_name).with_suffix(".png"),
            (image_dir / image_name).with_suffix(".png"),
        )

    # Update language_model_weight in parameters.yml
    model_path = tmp_path / "models"
    model_path.mkdir(exist_ok=True)

    shutil.copyfile(
        PREDICTION_DATA_PATH / "model.pt",
        model_path / "model.pt",
    )
    shutil.copyfile(
        PREDICTION_DATA_PATH / "charset.pkl",
        model_path / "charset.pkl",
    )

    params = read_yaml(PREDICTION_DATA_PATH / "parameters.yml")
    params["parameters"]["language_model"]["weight"] = language_model_weight
    yaml.dump(params, (model_path / "parameters.yml").open("w"))

    run_prediction(
        image_dir=image_dir,
        font=FONT_PATH,
        maximum_font_size=MAXIMUM_FONT_SIZE,
        model=model_path,
        output=tmp_path,
        confidence_score=False,
        confidence_score_levels=[],
        attention_map=[],
        attention_map_level=None,
        attention_map_scale=0.5,
        alpha_factor=0.9,
        color_map="nipy_spectral",
        word_separators=[" ", "\n"],
        line_separators=["\n"],
        temperature=1.0,
        predict_objects=False,
        max_object_height=None,
        image_extension=".png",
        gpu_device=None,
        batch_size=1,
        tokens=parse_tokens(PREDICTION_DATA_PATH / "tokens.yml"),
        start_token=None,
        use_language_model=True,
        compile_model=False,
        dynamic_mode=False,
    )

    for image_name, expected_prediction in zip(image_names, expected_predictions):
        prediction = json.loads(
            (tmp_path / image_name).with_suffix(".json").read_text()
        )
        assert prediction["text"] == expected_prediction["text"]

        if language_model_weight > 0:
            assert (
                prediction["language_model"]["text"]
                == expected_prediction["language_model"]["text"]
            )
            assert np.isclose(
                prediction["language_model"]["confidence"],
                expected_prediction["language_model"]["confidence"],
            )
