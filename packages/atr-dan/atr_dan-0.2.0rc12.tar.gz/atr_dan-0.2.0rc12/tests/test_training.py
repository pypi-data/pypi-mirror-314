# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

from operator import attrgetter

import pytest
import torch
import yaml

from dan.ocr.train import train
from dan.ocr.utils import build_batch_sizes, update_config
from tests.conftest import FIXTURES


@pytest.mark.parametrize(
    "batch_size, expected_batch_sizes",
    [
        (1, [1]),
        # Odd
        (13, [13, 6, 4, 2, 1]),  # The second number is not a multiple of 4
        (15, [15, 8, 4, 2, 1]),  # The second number is a multiple of 4
        # Even
        (12, [12, 6, 4, 2, 1]),  # The second number is not a multiple of 4
        (64, [64, 32, 16, 8, 4, 2, 1]),  # The second number is a multiple of 4
    ],
)
def test_build_batch_sizes(batch_size, expected_batch_sizes):
    assert list(build_batch_sizes(batch_size)) == expected_batch_sizes


@pytest.mark.parametrize(
    "expected_best_model_name, expected_last_model_name, params_res",
    (
        (
            "best_0.pt",
            "last_3.pt",
            {
                "parameters": {
                    "max_char_prediction": 30,
                    "encoder": {"dropout": 0.5},
                    "decoder": {
                        "enc_dim": 256,
                        "l_max": 15000,
                        "h_max": 500,
                        "w_max": 1000,
                        "dec_num_layers": 8,
                        "dec_num_heads": 4,
                        "dec_res_dropout": 0.1,
                        "dec_pred_dropout": 0.1,
                        "dec_att_dropout": 0.1,
                        "dec_dim_feedforward": 256,
                        "vocab_size": 96,
                        "attention_win": 100,
                    },
                    "preprocessings": [
                        {
                            "max_height": 2000,
                            "max_width": 2000,
                            "type": "max_resize",
                        }
                    ],
                    "mean": [
                        242.10595854671013,
                        242.10595854671013,
                        242.10595854671013,
                    ],
                    "std": [28.29919517652322, 28.29919517652322, 28.29919517652322],
                },
            },
        ),
    ),
)
def test_train(
    expected_best_model_name,
    expected_last_model_name,
    params_res,
    training_config,
    tmp_path,
):
    update_config(training_config)

    # Use the tmp_path as base folder
    training_config["training"]["output_folder"] = (
        tmp_path / training_config["training"]["output_folder"]
    )

    train(0, training_config)

    # There should only be two checkpoints left
    checkpoints = (
        tmp_path / training_config["training"]["output_folder"] / "checkpoints"
    )

    # Make sure we only have these two checkpoints
    assert sorted(map(attrgetter("name"), checkpoints.iterdir())) == [
        expected_best_model_name,
        expected_last_model_name,
    ]

    # Check that the trained model is correct
    for model_name in [expected_best_model_name, expected_last_model_name]:
        expected_model = torch.load(FIXTURES / "training" / "models" / model_name)
        trained_model = torch.load(
            checkpoints / model_name,
        )

        # Check the optimizers parameters
        for trained, expected in zip(
            trained_model["optimizers_named_params"]["encoder"],
            expected_model["optimizers_named_params"]["encoder"],
        ):
            for (trained_param, trained_tensor), (
                expected_param,
                expected_tensor,
            ) in zip(trained.items(), expected.items()):
                assert trained_param == expected_param
                assert torch.allclose(
                    trained_tensor, expected_tensor, rtol=1e-05, atol=1e-03
                )

        # Check the optimizer encoder and decoder state dicts
        for optimizer_part in [
            "optimizer_encoder_state_dict",
            "optimizer_decoder_state_dict",
        ]:
            for trained, expected in zip(
                trained_model[optimizer_part]["state"].values(),
                expected_model[optimizer_part]["state"].values(),
            ):
                for (trained_param, trained_tensor), (
                    expected_param,
                    expected_tensor,
                ) in zip(trained.items(), expected.items()):
                    assert trained_param == expected_param
                    assert torch.allclose(
                        trained_tensor,
                        expected_tensor,
                        atol=1e-03,
                    )
            assert (
                trained_model[optimizer_part]["param_groups"]
                == expected_model[optimizer_part]["param_groups"]
            )

        # Check the encoder and decoder weights
        for model_part in ["encoder_state_dict", "decoder_state_dict"]:
            for (trained_name, trained_layer), (expected_name, expected_layer) in zip(
                trained_model[model_part].items(), expected_model[model_part].items()
            ):
                assert trained_name == expected_name
                assert torch.allclose(
                    trained_layer,
                    expected_layer,
                    atol=1e-03,
                )

        # Check the other information
        for elt in [
            "epoch",
            "step",
            "scaler_state_dict",
            "best",
            "charset",
            "curriculum_config",
        ]:
            assert trained_model[elt] == expected_model[elt]

    # Check that the inference parameters file is correct
    res = yaml.safe_load(
        (
            tmp_path
            / training_config["training"]["output_folder"]
            / "results"
            / "inference_parameters.yml"
        ).read_text()
    )
    assert res == params_res
