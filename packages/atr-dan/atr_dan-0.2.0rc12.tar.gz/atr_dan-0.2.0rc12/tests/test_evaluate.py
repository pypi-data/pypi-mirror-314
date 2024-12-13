# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import json
import shutil
from pathlib import Path

import pytest
import yaml
from prettytable import PrettyTable

from dan.ocr import evaluate
from dan.ocr.manager.metrics import Inference
from dan.ocr.utils import add_metrics_table_row, create_metrics_table
from tests import FIXTURES

PREDICTION_DATA_PATH = FIXTURES / "prediction"


def test_create_metrics_table():
    metric_names = ["ignored", "wer", "cer", "time", "ner"]
    metrics_table = create_metrics_table(metric_names)

    assert isinstance(metrics_table, PrettyTable)
    assert metrics_table.field_names == [
        "Split",
        "CER (HTR-NER)",
        "WER (HTR-NER)",
        "NER",
    ]


def test_add_metrics_table_row():
    metric_names = ["ignored", "wer", "cer", "time", "ner"]
    metrics_table = create_metrics_table(metric_names)

    metrics = {
        "ignored": "whatever",
        "wer": 1.0,
        "cer": 1.3023,
        "time": 42,
    }
    add_metrics_table_row(metrics_table, "train", metrics)

    assert isinstance(metrics_table, PrettyTable)
    assert metrics_table.field_names == [
        "Split",
        "CER (HTR-NER)",
        "WER (HTR-NER)",
        "NER",
    ]
    assert metrics_table.rows == [["train", 130.23, 100, "−"]]


def test_print_worst_predictions(capsys):
    evaluate.print_worst_predictions(
        all_inferences={
            "test": [
                Inference(
                    image="0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84.png",
                    ground_truth="ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier Ⓟ12241",
                    prediction="ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    lm_prediction="ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    wer=0.125,
                ),
                # Test with empty strings
                Inference(
                    image="0dfe8bcd-ed0b-453e-bf19-cc697012296e.png",
                    ground_truth="Some text",
                    prediction="",
                    lm_prediction="",
                    wer=1,
                ),
                Inference(
                    image="2c242f5c-e979-43c4-b6f2-a6d4815b651d.png",
                    ground_truth="",
                    prediction="Some text",
                    lm_prediction="",
                    wer=1,
                ),
                Inference(
                    image="ffdec445-7f14-4f5f-be44-68d0844d0df1.png",
                    ground_truth="",
                    prediction="",
                    lm_prediction="Some text",
                    wer=0,
                ),
            ]
        }
    )

    # Check the metrics Markdown table
    captured_std = capsys.readouterr()
    last_printed_lines = captured_std.out.split("\n")
    assert (
        "\n".join(last_printed_lines)
        == Path(FIXTURES / "evaluate" / "worst_predictions.md").read_text()
    )


def test_eval_nerval(capsys, evaluate_config):
    evaluate.eval_nerval(
        all_inferences={
            "test": [
                Inference(
                    image="0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84.png",
                    ground_truth="ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier Ⓟ12241",
                    prediction="ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    lm_prediction="ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",
                    wer=0.125,
                ),
                # Test with empty strings
                Inference(
                    image="0dfe8bcd-ed0b-453e-bf19-cc697012296e.png",
                    ground_truth="Some text",
                    prediction="",
                    lm_prediction="",
                    wer=1,
                ),
                Inference(
                    image="2c242f5c-e979-43c4-b6f2-a6d4815b651d.png",
                    ground_truth="",
                    prediction="Some text",
                    lm_prediction="",
                    wer=1,
                ),
                Inference(
                    image="ffdec445-7f14-4f5f-be44-68d0844d0df1.png",
                    ground_truth="",
                    prediction="",
                    lm_prediction="Some text",
                    wer=0,
                ),
            ]
        },
        tokens=evaluate_config["dataset"]["tokens"],
        threshold=evaluate.NERVAL_THRESHOLD,
    )

    # Check the metrics Markdown table
    captured_std = capsys.readouterr()
    last_printed_lines = captured_std.out.split("\n")
    assert (
        "\n".join(last_printed_lines)
        == Path(FIXTURES / "evaluate" / "eval_nerval.md").read_text()
    )


@pytest.mark.parametrize(
    "training_res, val_res, test_res",
    (
        (
            {
                "nb_chars": 90,
                "cer": 0.1889,
                "nb_chars_no_token": 76,
                "cer_no_token": 0.2105,
                "nb_words": 15,
                "wer": 0.2667,
                "nb_words_no_punct": 15,
                "wer_no_punct": 0.2667,
                "nb_words_no_token": 15,
                "wer_no_token": 0.2667,
                "nb_tokens": 14,
                "ner": 0.0714,
                "nb_samples": 2,
            },
            {
                "nb_chars": 34,
                "cer": 0.0882,
                "nb_chars_no_token": 26,
                "cer_no_token": 0.1154,
                "nb_words": 8,
                "wer": 0.5,
                "nb_words_no_punct": 8,
                "wer_no_punct": 0.5,
                "nb_words_no_token": 8,
                "wer_no_token": 0.5,
                "nb_tokens": 8,
                "ner": 0.0,
                "nb_samples": 1,
            },
            {
                "nb_chars": 36,
                "cer": 0.0278,
                "nb_chars_no_token": 30,
                "cer_no_token": 0.0333,
                "nb_words": 7,
                "wer": 0.1429,
                "nb_words_no_punct": 7,
                "wer_no_punct": 0.1429,
                "nb_words_no_token": 7,
                "wer_no_token": 0.1429,
                "nb_tokens": 6,
                "ner": 0.0,
                "nb_samples": 1,
            },
        ),
    ),
)
@pytest.mark.parametrize("is_output_json", ((True, False)))
def test_evaluate(
    capsys, training_res, val_res, test_res, is_output_json, evaluate_config, tmp_path
):
    evaluate_path = FIXTURES / "evaluate"

    # Use the tmp_path as base folder
    evaluate_config["training"]["output_folder"] = evaluate_path

    output_json = tmp_path / "inference.json" if is_output_json else None

    evaluate_config["training"]["validation"]["font"] = "fonts/LinuxLibertine.ttf"
    evaluate_config["training"]["validation"]["maximum_font_size"] = 32
    evaluate_config["training"]["validation"]["nb_logged_images"] = 5

    evaluate.run(evaluate_config, evaluate.NERVAL_THRESHOLD, output_json=output_json)

    if is_output_json:
        assert json.loads(output_json.read_text()) == json.loads(
            (evaluate_path / "inference.json").read_text()
        )

    # Check that the evaluation results are correct
    for split_name, expected_res in zip(
        ["train", "val", "test"], [training_res, val_res, test_res]
    ):
        filename = (
            evaluate_config["training"]["output_folder"]
            / "results"
            / f"predict_training-{split_name}_1685.yaml"
        )

        assert {
            metric: value
            for metric, value in yaml.safe_load(filename.read_bytes()).items()
            # Remove the times from the results as they vary
            if "time" not in metric
        } == expected_res

    # Remove results files
    shutil.rmtree(evaluate_config["training"]["output_folder"] / "results")

    # Check the metrics Markdown table
    captured_std = capsys.readouterr()
    last_printed_lines = captured_std.out.split("\n")[10:]
    assert (
        "\n".join(last_printed_lines)
        == Path(FIXTURES / "evaluate" / "metrics_table.md").read_text()
    )


@pytest.mark.parametrize(
    "language_model_weight, expected_inferences",
    (
        (
            0.0,
            [
                (
                    "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84.png",  # Image
                    "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier Ⓟ12241",  # Ground truth
                    "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",  # Prediction
                    "",  # LM prediction
                    0.125,  # WER
                ),
                (
                    "0dfe8bcd-ed0b-453e-bf19-cc697012296e.png",  # Image
                    "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁJ Ⓚch ⓄE dachyle",  # Ground truth
                    "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",  # Prediction
                    "",  # LM prediction
                    0.4286,  # WER
                ),
                (
                    "2c242f5c-e979-43c4-b6f2-a6d4815b651d.png",  # Image
                    "ⓈA ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF ⓄA Ⓟ14331",  # Ground truth
                    "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31",  # Prediction
                    "",  # LM prediction
                    0.5,  # WER
                ),
                (
                    "ffdec445-7f14-4f5f-be44-68d0844d0df1.png",  # Image
                    "ⓈNaudin ⒻMarie Ⓑ53 ⓁS ⒸV ⓀBelle mère",  # Ground truth
                    "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",  # Prediction
                    "",  # LM prediction
                    0.1429,  # WER
                ),
            ],
        ),
        (
            1.0,
            [
                (
                    "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84.png",  # Image
                    "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier Ⓟ12241",  # Ground truth
                    "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",  # Prediction
                    "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",  # LM prediction
                    0.125,  # WER
                ),
                (
                    "0dfe8bcd-ed0b-453e-bf19-cc697012296e.png",  # Image
                    "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁJ Ⓚch ⓄE dachyle",  # Ground truth
                    "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",  # Prediction
                    "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",  # LM prediction
                    0.4286,  # WER
                ),
                (
                    "2c242f5c-e979-43c4-b6f2-a6d4815b651d.png",  # Image
                    "ⓈA ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF ⓄA Ⓟ14331",  # Ground truth
                    "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31",  # Prediction
                    "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31",  # LM prediction
                    0.5,  # WER
                ),
                (
                    "ffdec445-7f14-4f5f-be44-68d0844d0df1.png",  # Image
                    "ⓈNaudin ⒻMarie Ⓑ53 ⓁS ⒸV ⓀBelle mère",  # Ground truth
                    "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",  # Prediction
                    "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",  # LM prediction
                    0.1429,  # WER
                ),
            ],
        ),
        (
            2.0,
            [
                (
                    "0a56e8b3-95cd-4fa5-a17b-5b0ff9e6ea84.png",  # Image
                    "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier Ⓟ12241",  # Ground truth
                    "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",  # Prediction
                    "ⓈBellisson ⒻGeorges Ⓑ91 ⓁP ⒸM ⓀCh ⓄPlombier ⓅPatron?12241",  # LM prediction
                    0.125,  # WER
                ),
                (
                    "0dfe8bcd-ed0b-453e-bf19-cc697012296e.png",  # Image
                    "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁJ Ⓚch ⓄE dachyle",  # Ground truth
                    "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",  # Prediction
                    "ⓈTemplié ⒻMarcelle Ⓑ93 ⓁS Ⓚch ⓄE dactylo Ⓟ18376",  # LM prediction
                    0.4286,  # WER
                ),
                (
                    "2c242f5c-e979-43c4-b6f2-a6d4815b651d.png",  # Image
                    "ⓈA ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF ⓄA Ⓟ14331",  # Ground truth
                    "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14 31",  # Prediction
                    "Ⓢd ⒻCharles Ⓑ11 ⓁP ⒸC ⓀF Ⓞd Ⓟ14331",  # LM prediction
                    0.5,  # WER
                ),
                (
                    "ffdec445-7f14-4f5f-be44-68d0844d0df1.png",  # Image
                    "ⓈNaudin ⒻMarie Ⓑ53 ⓁS ⒸV ⓀBelle mère",  # Ground truth
                    "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",  # Prediction
                    "ⓈNaudin ⒻMarie Ⓑ53 ⓁS Ⓒv ⓀBelle mère",  # LM prediction
                    0.1429,  # WER
                ),
            ],
        ),
    ),
)
def test_evaluate_language_model(
    capsys, evaluate_config, language_model_weight, expected_inferences, monkeypatch
):
    # LM predictions are never used/displayed
    # We mock the `Inference` class to temporary check the results
    global nb_inferences
    nb_inferences = 0

    class MockInference(Inference):
        def __new__(cls, *args, **kwargs):
            global nb_inferences
            assert args == expected_inferences[nb_inferences]
            nb_inferences += 1

            return super().__new__(cls, *args, **kwargs)

    monkeypatch.setattr("dan.ocr.manager.training.Inference", MockInference)

    # Use the tmp_path as base folder
    evaluate_config["training"]["output_folder"] = FIXTURES / "evaluate"

    # Use a LM decoder
    evaluate_config["model"]["lm"] = {
        "path": PREDICTION_DATA_PATH / "language_model.arpa",
        "weight": language_model_weight,
    }

    evaluate_config["training"]["validation"]["font"] = "fonts/LinuxLibertine.ttf"
    evaluate_config["training"]["validation"]["maximum_font_size"] = 32
    evaluate_config["training"]["validation"]["nb_logged_images"] = 5

    evaluate.run(evaluate_config, evaluate.NERVAL_THRESHOLD, output_json=None)

    # Check that the evaluation results are correct
    for split_name, expected_res in [
        (
            "train",
            {
                "nb_chars": 90,
                "cer": 0.1889,
                "nb_chars_no_token": 76,
                "cer_no_token": 0.2105,
                "nb_words": 15,
                "wer": 0.2667,
                "nb_words_no_punct": 15,
                "wer_no_punct": 0.2667,
                "nb_words_no_token": 15,
                "wer_no_token": 0.2667,
                "nb_tokens": 14,
                "ner": 0.0714,
                "nb_samples": 2,
            },
        ),
        (
            "val",
            {
                "nb_chars": 34,
                "cer": 0.0882,
                "nb_chars_no_token": 26,
                "cer_no_token": 0.1154,
                "nb_words": 8,
                "wer": 0.5,
                "nb_words_no_punct": 8,
                "wer_no_punct": 0.5,
                "nb_words_no_token": 8,
                "wer_no_token": 0.5,
                "nb_tokens": 8,
                "ner": 0.0,
                "nb_samples": 1,
            },
        ),
        (
            "test",
            {
                "nb_chars": 36,
                "cer": 0.0278,
                "nb_chars_no_token": 30,
                "cer_no_token": 0.0333,
                "nb_words": 7,
                "wer": 0.1429,
                "nb_words_no_punct": 7,
                "wer_no_punct": 0.1429,
                "nb_words_no_token": 7,
                "wer_no_token": 0.1429,
                "nb_tokens": 6,
                "ner": 0.0,
                "nb_samples": 1,
            },
        ),
    ]:
        filename = (
            evaluate_config["training"]["output_folder"]
            / "results"
            / f"predict_training-{split_name}_1685.yaml"
        )

        with filename.open() as f:
            assert {
                metric: value
                for metric, value in yaml.safe_load(f).items()
                # Remove the times from the results as they vary
                if "time" not in metric
            } == expected_res

    # Remove results files
    shutil.rmtree(evaluate_config["training"]["output_folder"] / "results")

    # Check the metrics Markdown table
    captured_std = capsys.readouterr()
    last_printed_lines = captured_std.out.split("\n")[10:]
    assert (
        "\n".join(last_printed_lines)
        == Path(FIXTURES / "evaluate" / "metrics_table.md").read_text()
    )
