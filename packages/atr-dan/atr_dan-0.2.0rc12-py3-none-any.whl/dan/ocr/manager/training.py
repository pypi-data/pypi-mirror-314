# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import logging
import os
import random
from copy import deepcopy
from enum import Enum
from itertools import repeat
from pathlib import Path
from time import time
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import yaml
from torch.cuda.amp import GradScaler, autocast
from torch.nn import CrossEntropyLoss
from torch.nn.init import kaiming_uniform_
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.tensorboard import SummaryWriter
from torchvision.transforms import Compose, PILToTensor
from tqdm import tqdm

from dan.ocr import wandb
from dan.ocr.decoder import CTCLanguageDecoder, GlobalHTADecoder
from dan.ocr.encoder import FCN_Encoder
from dan.ocr.manager.metrics import Inference, MetricManager
from dan.ocr.manager.ocr import OCRDatasetManager
from dan.ocr.mlflow import MLFLOW_AVAILABLE, logging_metrics, logging_tags_metrics
from dan.ocr.schedulers import DropoutScheduler
from dan.ocr.utils import create_image
from dan.utils import fix_ddp_layers_names, ind_to_token

if MLFLOW_AVAILABLE:
    import mlflow

logger = logging.getLogger(__name__)

MODEL_NAME_ENCODER = "encoder"
MODEL_NAME_DECODER = "decoder"
MODEL_NAMES = (MODEL_NAME_ENCODER, MODEL_NAME_DECODER)


class GenericTrainingManager:
    def __init__(self, params):
        self.type = None
        self.is_master = False
        self.params = params
        self.models = {}
        self.dataset = None
        self.dataset_name = list(self.params["dataset"]["datasets"].values())[0]
        self.paths = None
        self.latest_step = 0
        self.latest_epoch = -1

        self.scaler = None

        self.font = self.params["training"]["validation"]["font"]
        self.maximum_font_size = self.params["training"]["validation"][
            "maximum_font_size"
        ]
        self.nb_logged_images = self.params["training"]["validation"][
            "nb_logged_images"
        ]

        self.optimizers = dict()
        self.optimizers_named_params_by_group = dict()
        self.lr_schedulers = dict()
        self.best = None
        self.writer = None
        self.metric_manager = dict()

        self.device_params = self.params["training"]["device"]
        self.nb_gpu = (
            self.device_params["nb_gpu"]
            if self.device_params["use_ddp"]
            else torch.cuda.device_count()
        )
        # Number of worker that process. Set to the number of GPU available if we are using DDP. Otherwise set to 1.
        self.nb_workers = self.nb_gpu if self.device_params["use_ddp"] else 1
        self.tokens = self.params["dataset"].get("tokens")

        self.init_hardware_config()
        self.init_paths()
        self.load_dataset()

    @property
    def encoder(self) -> FCN_Encoder | None:
        return self.models.get(MODEL_NAME_ENCODER)

    @property
    def decoder(self) -> GlobalHTADecoder | None:
        return self.models.get(MODEL_NAME_DECODER)

    def init_paths(self):
        """
        Create output folders for results and checkpoints
        """
        output_path = self.params["training"]["output_folder"]
        checkpoints_path = output_path / "checkpoints"
        results_path = output_path / "results"

        # Create folder
        checkpoints_path.mkdir(parents=True, exist_ok=True)
        results_path.mkdir(exist_ok=True)

        self.paths: Dict[str, Path] = {
            "results": results_path,
            "checkpoints": checkpoints_path,
            "output_folder": output_path,
        }

    def load_dataset(self):
        """
        Load datasets, data samplers and data loaders
        """
        self.dataset = OCRDatasetManager(
            dataset_params=self.params["dataset"],
            training_params=self.params["training"],
            device=self.device,
        )
        self.dataset.load_datasets()
        self.dataset.load_ddp_samplers()
        self.dataset.load_dataloaders()

    def init_hardware_config(self):
        cuda_is_available = torch.cuda.is_available()

        # Debug mode
        if self.device_params["force"] not in [None, "cuda"] or not cuda_is_available:
            self.device_params["use_ddp"] = False
            self.device_params["use_amp"] = False

        # Manage Distributed Data Parallel & GPU usage
        self.manual_seed = self.params["training"].get("manual_seed", 1111)
        self.ddp_config = {
            "master": self.device_params["use_ddp"]
            and self.device_params["ddp_rank"] == 0,
            "address": self.device_params.get("ddp_addr", "localhost"),
            "port": self.device_params.get("ddp_addr", "11111"),
            "backend": self.device_params.get("ddp_backend", "nccl"),
            "rank": self.device_params["ddp_rank"],
        }
        self.is_master = self.ddp_config["master"] or not self.device_params["use_ddp"]
        if self.device_params["use_ddp"]:
            self.device = torch.device(self.ddp_config["rank"])
            self.device_params["ddp_rank"] = self.ddp_config["rank"]
            self.launch_ddp()
        else:
            self.device = torch.device(
                self.device_params["force"] or "cuda" if cuda_is_available else "cpu"
            )
        if self.device == torch.device("cpu"):
            self.params["model"]["device"] = "cpu"
        else:
            self.params["model"]["device"] = self.device.type
        # Print GPU info
        # global
        if self.ddp_config["master"] or not self.device_params["use_ddp"]:
            print("##################")
            print("Available GPUS: {}".format(self.nb_gpu))
            for i in range(self.nb_gpu):
                print(
                    "Rank {}: {} {}".format(
                        i,
                        torch.cuda.get_device_name(i),
                        torch.cuda.get_device_properties(i),
                    )
                )
            print("##################")
        # local
        print("Local GPU:")
        if self.device != torch.device("cpu"):
            print(
                "Rank {}: {} {}".format(
                    self.device_params["ddp_rank"],
                    torch.cuda.get_device_name(),
                    torch.cuda.get_device_properties(self.device),
                )
            )
        else:
            print("WORKING ON CPU !\n")
        print("##################")

    def load_model(self, reset_optimizer=False, strict=True):
        """
        Load model weights from scratch or from checkpoints
        """
        common_params = {
            "h_max": self.params["model"].get("h_max"),
            "w_max": self.params["model"].get("w_max"),
            "device": self.device,
            "vocab_size": self.params["model"]["vocab_size"],
        }
        # Instantiate encoder, decoder
        for model_name in MODEL_NAMES:
            params = self.params["model"][model_name]
            model_class = params.get("class")
            self.models[model_name] = model_class({**params, **common_params})
            self.models[model_name].to(self.device)  # To GPU or CPU
            # make the model compatible with Distributed Data Parallel if used
            if self.device_params["use_ddp"]:
                self.models[model_name] = DDP(
                    self.models[model_name],
                    [self.ddp_config["rank"]],
                    output_device=self.ddp_config["rank"],
                )

        # Instantiate LM decoder
        self.lm_decoder = None
        if self.params["model"].get("lm") and self.params["model"]["lm"]["weight"] > 0:
            logger.info(
                f"Decoding with a language model (weight={self.params['model']['lm']['weight']})."
            )
            # Check files
            model_path = self.params["model"]["lm"]["path"]
            assert model_path.is_file(), f"File {model_path} not found"
            base_path = model_path.parent
            lexicon_path = base_path / "lexicon.txt"
            assert lexicon_path.is_file(), f"File {lexicon_path} not found"
            tokens_path = base_path / "tokens.txt"
            assert tokens_path.is_file(), f"File {tokens_path} not found"
            # Load LM decoder
            self.lm_decoder = CTCLanguageDecoder(
                language_model_path=str(model_path),
                lexicon_path=str(lexicon_path),
                tokens_path=str(tokens_path),
                language_model_weight=self.params["model"]["lm"]["weight"],
            )

        # Handle curriculum dropout
        self.dropout_scheduler = DropoutScheduler(self.models)

        self.scaler = GradScaler(enabled=self.device_params["use_amp"])

        # Check if checkpoint exists
        checkpoint = self.get_checkpoint()
        if checkpoint is not None:
            self.load_existing_model(checkpoint, strict=strict)
        else:
            self.init_new_model()

        self.load_optimizers(checkpoint, reset_optimizer=reset_optimizer)

        if self.is_master:
            print("LOADED EPOCH: {}\n".format(self.latest_epoch), flush=True)

    def get_checkpoint(self):
        """
        Seek if checkpoint exist, return None otherwise
        """
        if self.params["training"]["load_epoch"] in ("best", "last"):
            for filename in self.paths["checkpoints"].iterdir():
                if self.params["training"]["load_epoch"] in filename.name:
                    return torch.load(
                        filename,
                        map_location=self.device,
                    )
        return None

    def load_existing_model(self, checkpoint, strict=True):
        """
        Load information and weights from previous training
        """
        self.load_save_info(checkpoint)
        self.latest_epoch = checkpoint["epoch"]
        if "step" in checkpoint:
            self.latest_step = checkpoint["step"]
        self.best = checkpoint["best"]
        if "scaler_state_dict" in checkpoint:
            self.scaler.load_state_dict(checkpoint["scaler_state_dict"])
        if "dropout_scheduler_step" in checkpoint:
            self.dropout_scheduler.resume(checkpoint["dropout_scheduler_step"])
        # Load model weights from past training
        for model_name in self.models:
            # Transform to DDP/from DDP model
            checkpoint[f"{model_name}_state_dict"] = fix_ddp_layers_names(
                checkpoint[f"{model_name}_state_dict"],
                self.device_params["use_ddp"],
            )

            self.models[model_name].load_state_dict(
                checkpoint[f"{model_name}_state_dict"], strict=strict
            )

    def init_new_model(self):
        """
        Initialize model
        """
        # Specific weights initialization if exists
        for model_name in self.models:
            try:
                self.models[model_name].init_weights()
            except Exception:
                pass

        # Handle transfer learning instructions
        if self.params["training"]["transfer_learning"]:
            # Iterates over models
            for model_name in self.params["training"]["transfer_learning"]:
                state_dict_name, path, learnable, strict = self.params["training"][
                    "transfer_learning"
                ][model_name]

                # Loading pretrained weights file
                checkpoint = torch.load(path, map_location=self.device)
                # Transform to DDP/from DDP model
                checkpoint[f"{model_name}_state_dict"] = fix_ddp_layers_names(
                    checkpoint[f"{model_name}_state_dict"],
                    self.device_params["use_ddp"],
                )

                try:
                    # Load pretrained weights for model
                    self.models[model_name].load_state_dict(
                        checkpoint["{}_state_dict".format(state_dict_name)],
                        strict=strict,
                    )
                    print(
                        "transferred weights for {}".format(state_dict_name), flush=True
                    )
                except RuntimeError as e:
                    print(e, flush=True)
                    # if error, try to load each parts of the model (useful if only few layers are different)
                    for key in checkpoint[
                        "{}_state_dict".format(state_dict_name)
                    ].keys():
                        try:
                            # for pre-training of decision layer
                            if (
                                "end_conv" in key
                                and "transfered_charset" in self.params["model"]
                                and self.params["model"]["transfered_charset"]
                            ):
                                self.adapt_decision_layer_to_old_charset(
                                    model_name, key, checkpoint, state_dict_name
                                )
                            else:
                                self.models[model_name].load_state_dict(
                                    {
                                        key: checkpoint[
                                            "{}_state_dict".format(state_dict_name)
                                        ][key]
                                    },
                                    strict=False,
                                )
                        except RuntimeError as e:
                            # exception when adding linebreak token from pretraining
                            print(e, flush=True)
                # Set parameters no trainable
                if not learnable:
                    self.set_model_learnable(self.models[model_name], False)

    def adapt_decision_layer_to_old_charset(
        self, model_name, key, checkpoint, state_dict_name
    ):
        """
        Transfer learning of the decision learning in case of close charsets between pre-training and training
        """
        pretrained_chars = list()
        weights = checkpoint["{}_state_dict".format(state_dict_name)][key]
        new_size = list(weights.size())
        new_size[0] = (
            len(self.dataset.charset) + self.params["model"]["additional_tokens"]
        )
        new_weights = torch.zeros(new_size, device=weights.device, dtype=weights.dtype)
        old_charset = (
            checkpoint["charset"]
            if "charset" in checkpoint
            else self.params["model"]["old_charset"]
        )
        if "bias" not in key:
            kaiming_uniform_(new_weights, nonlinearity="relu")
        for i, c in enumerate(self.dataset.charset):
            if c in old_charset:
                new_weights[i] = weights[old_charset.index(c)]
                pretrained_chars.append(c)
        checkpoint["{}_state_dict".format(state_dict_name)][key] = new_weights
        self.models[model_name].load_state_dict(
            {key: checkpoint["{}_state_dict".format(state_dict_name)][key]},
            strict=False,
        )
        print(
            "Pretrained chars for {} ({}): {}".format(
                key, len(pretrained_chars), pretrained_chars
            )
        )

    def load_optimizers(self, checkpoint, reset_optimizer=False):
        """
        Load the optimizer of each model
        """
        for model_name in self.models:
            if (
                checkpoint
                and "optimizer_named_params_{}".format(model_name) in checkpoint
            ):
                self.optimizers_named_params_by_group[model_name] = checkpoint[
                    "optimizer_named_params_{}".format(model_name)
                ]
            else:
                self.optimizers_named_params_by_group[model_name] = [
                    dict(),
                ]
                self.optimizers_named_params_by_group[model_name][0].update(
                    self.models[model_name].named_parameters()
                )

            # Instantiate optimizer
            self.reset_optimizer(model_name)

            # Handle learning rate schedulers
            if self.params["training"].get("lr_schedulers"):
                key = (
                    "all"
                    if "all" in self.params["training"]["lr_schedulers"]
                    else model_name
                )
                if key in self.params["training"]["lr_schedulers"]:
                    self.lr_schedulers[model_name] = self.params["training"][
                        "lr_schedulers"
                    ][key]["class"](
                        self.optimizers[model_name],
                        **self.params["training"]["lr_schedulers"][key]["args"],
                    )

            # Load optimizer state from past training
            if checkpoint and not reset_optimizer:
                self.optimizers[model_name].load_state_dict(
                    checkpoint["optimizer_{}_state_dict".format(model_name)]
                )
                # Load optimizer scheduler config from past training if used
                if (
                    "lr_schedulers" in self.params["training"]
                    and self.params["training"]["lr_schedulers"]
                    and "lr_scheduler_{}_state_dict".format(model_name) in checkpoint
                ):
                    self.lr_schedulers[model_name].load_state_dict(
                        checkpoint["lr_scheduler_{}_state_dict".format(model_name)]
                    )

    @staticmethod
    def set_model_learnable(model, learnable=True):
        for p in list(model.parameters()):
            p.requires_grad = learnable

    def save_model(self, epoch: int, name: str):
        """
        Save model weights and training info for curriculum learning or learning rate for instance
        """
        if not self.is_master:
            return

        path = self.paths["checkpoints"] / "{}_{}.pt".format(name, epoch)
        content = {
            "optimizers_named_params": self.optimizers_named_params_by_group,
            "epoch": epoch,
            "step": self.latest_step,
            "scaler_state_dict": self.scaler.state_dict(),
            "best": self.best,
            "charset": self.dataset.charset,
            "dropout_scheduler_step": self.dropout_scheduler.step_num,
        }

        for model_name in self.optimizers:
            content["optimizer_{}_state_dict".format(model_name)] = self.optimizers[
                model_name
            ].state_dict()

        for model_name in self.lr_schedulers:
            content[
                "lr_scheduler_{}_state_dict".format(model_name)
            ] = self.lr_schedulers[model_name].state_dict()

        content = self.add_save_info(content)
        for model_name in self.models:
            content["{}_state_dict".format(model_name)] = self.models[
                model_name
            ].state_dict()

        # Remove other checkpoints
        for path_to_del in self.paths["checkpoints"].glob(f"{name}_*.pt"):
            logger.warning(f"Removing checkpoint `{path_to_del}`")
            path_to_del.unlink()

        torch.save(content, path)

    def reset_optimizer(self, model_name):
        """
        Reset optimizer learning rate for given model
        """
        params = list(self.optimizers_named_params_by_group[model_name][0].values())
        key = "all" if "all" in self.params["training"]["optimizers"] else model_name
        self.optimizers[model_name] = self.params["training"]["optimizers"][key][
            "class"
        ](params, **self.params["training"]["optimizers"][key]["args"])
        for i in range(1, len(self.optimizers_named_params_by_group[model_name])):
            self.optimizers[model_name].add_param_group(
                {
                    "params": list(
                        self.optimizers_named_params_by_group[model_name][i].values()
                    )
                }
            )

    def save_params(self):
        """
        Output a yaml file containing a summary of all hyperparameters chosen for the training
        and a yaml file containing parameters used for inference
        """

        def compute_nb_params(module) -> np.int64:
            return sum([np.prod(p.size()) for p in list(module.parameters())])

        def class_to_str_dict(my_dict):
            for key in my_dict:
                if key == "preprocessings":
                    my_dict[key] = [
                        {
                            key: value.value if isinstance(value, Enum) else value
                            for key, value in preprocessing.items()
                        }
                        for preprocessing in my_dict[key]
                    ]
                elif callable(my_dict[key]):
                    my_dict[key] = my_dict[key].__name__
                elif isinstance(my_dict[key], np.ndarray):
                    my_dict[key] = my_dict[key].tolist()
                elif isinstance(my_dict[key], list) and isinstance(
                    my_dict[key][0], tuple
                ):
                    my_dict[key] = [list(elt) for elt in my_dict[key]]
                elif isinstance(my_dict[key], Path):
                    my_dict[key] = str(my_dict[key])
                elif isinstance(my_dict[key], dict):
                    my_dict[key] = class_to_str_dict(my_dict[key])
            return my_dict

        # Save training parameters
        path = self.paths["results"] / "training_parameters.yml"
        if path.is_file():
            return

        params = class_to_str_dict(my_dict=deepcopy(self.params))

        # Special case for transfer_learning parameter serialization
        if params["training"].get("transfer_learning"):
            for data in params["training"]["transfer_learning"].values():
                # The second item is a pathlib.Path object
                data[1] = str(data[1])

        total_params = 0
        for model_name in MODEL_NAMES:
            current_params = int(compute_nb_params(self.models[model_name]))
            params["model"][model_name]["nb_params"] = current_params
            total_params += current_params
        params["model"]["total_params"] = "{:,}".format(total_params)
        params["mean"] = self.dataset.mean.tolist()
        params["std"] = self.dataset.std.tolist()

        path.write_text(yaml.safe_dump(params))

        # Save inference parameters
        path = self.paths["results"] / "inference_parameters.yml"
        if path.is_file():
            return

        decoder_params = {
            key: params["model"]["decoder"][key]
            for key in (
                "l_max",
                "dec_num_layers",
                "dec_num_heads",
                "dec_res_dropout",
                "dec_pred_dropout",
                "dec_att_dropout",
                "dec_dim_feedforward",
                "attention_win",
                "enc_dim",
            )
        }

        inference_params = {
            "parameters": {
                "mean": params["mean"],
                "std": params["std"],
                "max_char_prediction": params["dataset"]["max_char_prediction"],
                "encoder": {"dropout": params["model"]["encoder"]["dropout"]},
                "decoder": {
                    "h_max": params["model"]["h_max"],
                    "w_max": params["model"]["w_max"],
                    "vocab_size": params["model"]["vocab_size"],
                    **decoder_params,
                },
                "preprocessings": params["training"]["data"]["preprocessings"],
            },
        }
        path.write_text(yaml.safe_dump(inference_params))

    def backward_loss(self, loss, retain_graph=False):
        self.scaler.scale(loss).backward(retain_graph=retain_graph)

    def step_optimizers(self, names=None):
        for model_name in self.optimizers:
            if names and model_name not in names:
                continue
            if (
                self.params["training"].get("gradient_clipping")
                and model_name in self.params["training"]["gradient_clipping"]["models"]
            ):
                self.scaler.unscale_(self.optimizers[model_name])
                torch.nn.utils.clip_grad_norm_(
                    self.models[model_name].parameters(),
                    self.params["training"]["gradient_clipping"]["max"],
                )
            self.scaler.step(self.optimizers[model_name])
        self.scaler.update()
        self.latest_step += 1

    def zero_optimizers(self, set_to_none=True):
        for model_name in self.optimizers:
            self.optimizers[model_name].zero_grad(set_to_none=set_to_none)

    def train(self, mlflow_logging=False):
        """
        Main training loop
        """
        # init tensorboard file and output param summary file
        if self.is_master:
            self.writer = SummaryWriter(self.paths["results"])
            self.save_params()

        # init variables
        nb_epochs = self.params["training"]["max_nb_epochs"]
        metric_names = self.params["training"]["metrics"]["train"]

        display_values = None
        # perform epochs
        for num_epoch in range(self.latest_epoch + 1, nb_epochs):
            # Whether we will evaluate this epoch
            evaluate_epoch = (
                self.params["training"]["validation"]["eval_on_valid"]
                and num_epoch
                % self.params["training"]["validation"]["eval_on_valid_interval"]
                == 0
            )

            # set models trainable
            for model_name in self.models:
                self.models[model_name].train()
            self.latest_epoch = num_epoch
            if self.dataset.train_dataset.curriculum_config:
                self.dataset.train_dataset.curriculum_config[
                    "epoch"
                ] = self.latest_epoch
            # init epoch metrics values
            self.metric_manager["train"] = MetricManager(
                metric_names=metric_names,
                dataset_name=self.dataset_name,
                tokens=self.tokens,
            )
            with tqdm(total=len(self.dataset.train_loader.dataset)) as pbar:
                pbar.set_description("EPOCH {}/{}".format(num_epoch, nb_epochs))
                # iterates over mini-batch data
                for ind_batch, batch_data in enumerate(self.dataset.train_loader):
                    # train on batch data and compute metrics
                    batch_values = self.train_batch(batch_data, metric_names)
                    batch_metrics = self.metric_manager["train"].compute_metrics(
                        batch_values, metric_names
                    )
                    batch_metrics["names"] = batch_data["names"]
                    # Merge metrics if Distributed Data Parallel is used
                    if self.device_params["use_ddp"]:
                        batch_metrics = self.merge_ddp_metrics(batch_metrics)
                    # Update learning rate via scheduler if one is used
                    if self.params["training"]["lr_schedulers"]:
                        for model_name in self.models:
                            key = (
                                "all"
                                if "all" in self.params["training"]["lr_schedulers"]
                                else model_name
                            )
                            if (
                                model_name in self.lr_schedulers
                                and ind_batch
                                % self.params["training"]["lr_schedulers"][key][
                                    "step_interval"
                                ]
                                == 0
                            ):
                                self.lr_schedulers[model_name].step(
                                    len(batch_metrics["names"])
                                )

                    # Update dropout scheduler
                    self.dropout_scheduler.step(len(batch_metrics["names"]))
                    self.dropout_scheduler.update_dropout_rate()

                    # Add batch metrics values to epoch metrics values
                    self.metric_manager["train"].update_metrics(batch_metrics)
                    display_values = self.metric_manager["train"].get_display_values()
                    pbar.set_postfix(values=str(display_values))
                    pbar.update(len(batch_data["names"]) * self.nb_workers)

                # Log MLflow metrics
                logging_metrics(
                    display_values, "train", num_epoch, mlflow_logging, self.is_master
                )

            if self.is_master:
                # Log metrics in tensorboard file
                for key in display_values:
                    self.writer.add_scalar(
                        "train/{}_{}".format(
                            self.params["dataset"]["train"]["name"], key
                        ),
                        display_values[key],
                        num_epoch,
                    )

                # Log "Weights & Biases" metrics
                wandb.log(
                    data={
                        f"train/{self.params['dataset']['train']['name']}_{key}": value
                        for key, value in display_values.items()
                    },
                    step=num_epoch,
                    # With "Weights & Biases" we can only publish once per step
                    # Do not commit now if data will be updated with the validation
                    commit=not evaluate_epoch,
                )

            # evaluate and compute metrics for valid sets
            if evaluate_epoch:
                for valid_set_name in self.dataset.valid_loaders:
                    # evaluate set and compute metrics
                    eval_values = self.validate(
                        valid_set_name, mlflow_logging=mlflow_logging
                    )

                    # Log metrics
                    if self.is_master:
                        # Log metrics in tensorboard file
                        for key in eval_values:
                            self.writer.add_scalar(
                                "valid/{}_{}".format(valid_set_name, key),
                                eval_values[key],
                                num_epoch,
                            )
                        if valid_set_name == self.params["training"]["validation"][
                            "set_name_focus_metric"
                        ] and (self.best is None or eval_values["cer"] <= self.best):
                            self.save_model(epoch=num_epoch, name="best")
                            self.best = eval_values["cer"]

                        # Log "Weights & Biases" metrics
                        wandb.log(
                            data={
                                f"valid/{valid_set_name}_{key}": value
                                for key, value in eval_values.items()
                            },
                            step=self.latest_epoch,
                            # With "Weights & Biases" we can only publish once per step
                            # Publish now because no data will be added for this step
                            commit=True,
                        )

            # save model weights
            if self.is_master:
                self.save_model(epoch=num_epoch, name="last")
                self.writer.flush()

    def validate(self, set_name, mlflow_logging=False, **kwargs):
        """
        Main loop for validation
        """
        loader = self.dataset.valid_loaders[set_name]
        # Set models in eval mode
        for model_name in self.models:
            self.models[model_name].eval()
        metric_names = self.params["training"]["metrics"]["eval"]
        display_values = None

        # initialize epoch metrics
        self.metric_manager[set_name] = MetricManager(
            metric_names=metric_names,
            dataset_name=self.dataset_name,
            tokens=self.tokens,
        )

        with tqdm(total=len(loader.dataset)) as pbar:
            pbar.set_description("VALID {} - {}".format(self.latest_epoch, set_name))
            with torch.no_grad():
                # iterate over batch data
                for ind_batch, batch_data in enumerate(loader):
                    # eval batch data and compute metrics
                    batch_values = self.evaluate_batch(batch_data, metric_names)
                    batch_metrics = self.metric_manager[set_name].compute_metrics(
                        batch_values, metric_names
                    )
                    batch_metrics["names"] = batch_data["names"]
                    # merge metrics values if Distributed Data Parallel is used
                    if self.device_params["use_ddp"]:
                        batch_metrics = self.merge_ddp_metrics(batch_metrics)

                    # add batch metrics to epoch metrics
                    self.metric_manager[set_name].update_metrics(batch_metrics)
                    display_values = self.metric_manager[set_name].get_display_values()

                    pbar.set_postfix(values=str(display_values))
                    pbar.update(len(batch_data["names"]) * self.nb_workers)

                    if ind_batch < self.nb_logged_images:
                        image = loader.dataset.get_sample_img(ind_batch)
                        result = create_image(
                            image,
                            batch_values["str_x"][0],
                            self.font,
                            self.maximum_font_size,
                            cer=round(batch_metrics["chars_error_rate"][0] * 100, 2),
                            wer=round(batch_metrics["words_error_rate"][0] * 100, 2),
                        )

                        result_tensor = Compose([PILToTensor()])(result)

                        self.writer.add_image(
                            f"valid_images/{batch_data['names'][0]}",
                            result_tensor,
                            self.latest_epoch,
                        )

                        # Log "Weights & Biases" metrics
                        if self.params.get("wandb", {}).get("images"):
                            wandb.image(
                                f"valid_images/{batch_data['names'][0]}",
                                result,
                                step=self.latest_epoch,
                                # With "Weights & Biases" we can only publish once per step
                                # Do not commit now because data will be updated with the validation metrics
                                commit=False,
                            )

                # log metrics in MLflow
                logging_metrics(
                    display_values,
                    "val",
                    self.latest_epoch,
                    mlflow_logging,
                    self.is_master,
                )
        return display_values

    def evaluate(
        self, custom_name, sets_list, metric_names, mlflow_logging=False
    ) -> Tuple[Dict[str, int | float], List[Inference]]:
        """
        Main loop for evaluation
        """
        metric_names = metric_names.copy()
        self.dataset.generate_test_loader(custom_name, sets_list)
        loader = self.dataset.test_loaders[custom_name]
        # Set models in eval mode
        for model_name in self.models:
            self.models[model_name].eval()

        # initialize epoch metrics
        self.metric_manager[custom_name] = MetricManager(
            metric_names=metric_names,
            dataset_name=self.dataset_name,
            tokens=self.tokens,
        )

        # Keep inferences in memory to:
        # - evaluate with Nerval
        # - display worst predictions
        inferences = []

        with tqdm(total=len(loader.dataset)) as pbar:
            pbar.set_description("Evaluation")
            with torch.no_grad():
                for ind_batch, batch_data in enumerate(loader):
                    # iterates over batch data
                    # eval batch data and compute metrics
                    batch_values = self.evaluate_batch(batch_data, metric_names)
                    batch_metrics = self.metric_manager[custom_name].compute_metrics(
                        batch_values, metric_names
                    )
                    batch_metrics["names"] = batch_data["names"]
                    # merge batch metrics if Distributed Data Parallel is used
                    if self.device_params["use_ddp"]:
                        batch_metrics = self.merge_ddp_metrics(batch_metrics)

                    # add batch metrics to epoch metrics
                    self.metric_manager[custom_name].update_metrics(batch_metrics)
                    display_values = self.metric_manager[
                        custom_name
                    ].get_display_values()

                    pbar.set_postfix(values=str(display_values))
                    pbar.update(len(batch_data["names"]) * self.nb_workers)
                    inferences.extend(
                        map(
                            Inference,
                            batch_data["names"],
                            batch_values["str_y"],
                            batch_values["str_x"],
                            batch_values.get("str_lm", repeat("")),
                            batch_metrics["words_error_rate"],
                        )
                    )

                # log metrics in MLflow
                logging_name = custom_name.split("-")[1]
                logging_tags_metrics(
                    display_values, logging_name, mlflow_logging, self.is_master
                )

        if "pred" in metric_names:
            self.output_pred(custom_name)
        metrics = self.metric_manager[custom_name].get_display_values(output=True)
        path = self.paths["results"] / "predict_{}_{}.yaml".format(
            custom_name, self.latest_epoch
        )
        path.write_text(yaml.dump(metrics))

        if mlflow_logging:
            # Log mlflow artifacts
            mlflow.log_artifact(path, "predictions")

        return metrics, inferences

    def output_pred(self, name):
        path = self.paths["results"] / "predict_{}_{}.yaml".format(
            name, self.latest_epoch
        )

        pred = "\n".join(self.metric_manager[name].get("pred"))
        path.write_text(yaml.dump(pred))

    def launch_ddp(self):
        """
        Initialize Distributed Data Parallel system
        """
        mp.set_start_method("fork", force=True)
        os.environ["MASTER_ADDR"] = self.ddp_config["address"]
        os.environ["MASTER_PORT"] = str(self.ddp_config["port"])
        dist.init_process_group(
            self.ddp_config["backend"],
            rank=self.ddp_config["rank"],
            world_size=self.nb_gpu,
        )
        torch.cuda.set_device(self.ddp_config["rank"])
        random.seed(self.manual_seed)
        np.random.seed(self.manual_seed)
        torch.manual_seed(self.manual_seed)
        torch.cuda.manual_seed(self.manual_seed)

    def merge_ddp_metrics(self, metrics):
        """
        Merge metrics when Distributed Data Parallel is used
        """
        for metric_name in metrics:
            if metric_name in [
                "edit_words",
                "nb_words",
                "edit_chars",
                "nb_chars",
                "edit_chars_force_len",
                "edit_chars_curr",
                "nb_chars_curr",
            ]:
                metrics[metric_name] = self.cat_ddp_metric(metrics[metric_name])
            elif metric_name in [
                "nb_samples",
                "loss",
                "loss_ce",
                "loss_ce_end",
            ]:
                metrics[metric_name] = self.sum_ddp_metric(
                    metrics[metric_name], average=False
                )
        return metrics

    def sum_ddp_metric(self, metric, average=False):
        """
        Sum metrics for Distributed Data Parallel
        """
        sum = torch.tensor(metric[0]).to(self.device)
        dist.all_reduce(sum, op=dist.ReduceOp.SUM)
        if average:
            sum.true_divide(dist.get_world_size())
        return [
            sum.item(),
        ]

    def cat_ddp_metric(self, metric):
        """
        Concatenate metrics for Distributed Data Parallel
        """
        tensor = torch.tensor(metric).unsqueeze(0).to(self.device)
        res = [
            torch.zeros(tensor.size()).long().to(self.device)
            for _ in range(dist.get_world_size())
        ]
        dist.all_gather(res, tensor)
        return list(torch.cat(res, dim=0).flatten().cpu().numpy())

    def train_batch(self, batch_data, metric_names):
        raise NotImplementedError

    def evaluate_batch(self, batch_data, metric_names):
        raise NotImplementedError

    def load_save_info(self, info_dict):
        """
        Load curriculum info from saved model info
        """
        if "curriculum_config" in info_dict:
            self.dataset.train_dataset.curriculum_config = info_dict[
                "curriculum_config"
            ]

    def add_save_info(self, info_dict):
        """
        Add curriculum info to model info to be saved
        """
        info_dict["curriculum_config"] = self.dataset.train_dataset.curriculum_config
        return info_dict


class Manager(GenericTrainingManager):
    def __init__(self, params):
        super(Manager, self).__init__(params)
        self.params["model"]["vocab_size"] = len(self.dataset.charset)

    def load_save_info(self, info_dict):
        if "curriculum_config" in info_dict:
            if self.dataset.train_dataset is not None:
                self.dataset.train_dataset.curriculum_config = info_dict[
                    "curriculum_config"
                ]

    def add_save_info(self, info_dict):
        info_dict["curriculum_config"] = self.dataset.train_dataset.curriculum_config
        return info_dict

    def add_label_noise(self, y, y_len, error_rate):
        y_error = y.clone()
        for b in range(len(y_len)):
            for i in range(1, y_len[b]):
                if (
                    np.random.rand() < error_rate
                    and y[b][i] != self.dataset.tokens["pad"]
                ):
                    y_error[b][i] = np.random.randint(0, len(self.dataset.charset) + 2)
        return y_error, y_len

    def train_batch(self, batch_data, metric_names):
        loss_func = CrossEntropyLoss(ignore_index=self.dataset.tokens["pad"])

        sum_loss = 0
        b = batch_data["imgs"].shape[0]
        batch_data["labels"] = batch_data["labels"].to(self.device)
        y_len = batch_data["labels_len"]

        if "label_noise_scheduler" in self.params["training"]:
            error_rate = (
                self.params["training"]["label_noise_scheduler"]["min_error_rate"]
                + min(
                    self.latest_step,
                    self.params["training"]["label_noise_scheduler"]["total_num_steps"],
                )
                * (
                    self.params["training"]["label_noise_scheduler"]["max_error_rate"]
                    - self.params["training"]["label_noise_scheduler"]["min_error_rate"]
                )
                / self.params["training"]["label_noise_scheduler"]["total_num_steps"]
            )
            simulated_y_pred, y_len = self.add_label_noise(
                batch_data["labels"], y_len, error_rate
            )
        else:
            simulated_y_pred = batch_data["labels"]

        with autocast(enabled=self.device_params["use_amp"]):
            hidden_predict = None
            cache = None

            features = self.encoder(batch_data["imgs"].to(self.device))
            features_size = features.size()

            if self.device_params["use_ddp"]:
                features = self.decoder.module.features_updater.get_pos_features(
                    features
                )
            else:
                features = self.decoder.features_updater.get_pos_features(features)
            features = torch.flatten(features, start_dim=2, end_dim=3).permute(2, 0, 1)

            output, pred, hidden_predict, cache, weights = self.decoder(
                features,
                simulated_y_pred[:, :-1],
                [s[:2] for s in batch_data["imgs_reduced_shape"]],
                [max(y_len) for _ in range(b)],
                features_size,
                start=0,
                hidden_predict=hidden_predict,
                cache=cache,
                keep_all_weights=True,
            )

            loss_ce = loss_func(pred, batch_data["labels"][:, 1:])
            sum_loss += loss_ce
            with autocast(enabled=False):
                self.backward_loss(sum_loss)
                self.step_optimizers()
                self.zero_optimizers()
            predicted_tokens = torch.argmax(pred, dim=1).detach().cpu().numpy()
            predicted_tokens = [predicted_tokens[i, : y_len[i]] for i in range(b)]
            str_x = [
                ind_to_token(self.dataset.charset, t, oov_symbol="")
                for t in predicted_tokens
            ]

        values = {
            "nb_samples": b,
            "str_y": batch_data["raw_labels"],
            "str_x": str_x,
            "loss": sum_loss.item(),
            "loss_ce": loss_ce.item(),
        }

        return values

    def evaluate_batch(self, batch_data, metric_names):
        x = batch_data["imgs"].to(self.device)

        max_chars = self.params["dataset"]["max_char_prediction"]

        start_time = time()
        with autocast(enabled=self.device_params["use_amp"]):
            b = x.size(0)
            reached_end = torch.zeros((b,), dtype=torch.bool, device=self.device)
            prediction_len = torch.zeros((b,), dtype=torch.int, device=self.device)
            predicted_tokens = (
                torch.ones((b, 1), dtype=torch.long, device=self.device)
                * self.dataset.tokens["start"]
            )
            predicted_tokens_len = torch.ones((b,), dtype=torch.int, device=self.device)

            # end token index will be used for ctc
            tot_pred = torch.zeros(
                (b, len(self.dataset.charset) + 1, max_chars),
                dtype=torch.float,
                device=self.device,
            )

            whole_output = list()
            confidence_scores = list()
            cache = None
            hidden_predict = None
            if b > 1:
                features_list = list()
                for i in range(b):
                    pos = batch_data["imgs_position"]
                    features_list.append(
                        self.encoder(
                            x[
                                i : i + 1,
                                :,
                                pos[i][0][0] : pos[i][0][1],
                                pos[i][1][0] : pos[i][1][1],
                            ]
                        )
                    )
                max_height = max([f.size(2) for f in features_list])
                max_width = max([f.size(3) for f in features_list])
                features = torch.zeros(
                    (b, features_list[0].size(1), max_height, max_width),
                    device=self.device,
                    dtype=features_list[0].dtype,
                )
                for i in range(b):
                    features[
                        i, :, : features_list[i].size(2), : features_list[i].size(3)
                    ] = features_list[i]
            else:
                features = self.encoder(x)
            features_size = features.size()

            if self.device_params["use_ddp"]:
                features = self.decoder.module.features_updater.get_pos_features(
                    features
                )
            else:
                features = self.decoder.features_updater.get_pos_features(features)
            features = torch.flatten(features, start_dim=2, end_dim=3).permute(2, 0, 1)

            for i in range(0, max_chars):
                output, pred, hidden_predict, cache, weights = self.decoder(
                    features,
                    predicted_tokens,
                    [s[:2] for s in batch_data["imgs_reduced_shape"]],
                    predicted_tokens_len,
                    features_size,
                    start=0,
                    hidden_predict=hidden_predict,
                    cache=cache,
                    num_pred=1,
                )

                # output total logit prediction
                tot_pred[:, :, i : i + 1] = pred

                whole_output.append(output)
                confidence_scores.append(
                    torch.max(torch.softmax(pred[:, :], dim=1), dim=1).values
                )
                predicted_tokens = torch.cat(
                    [
                        predicted_tokens,
                        torch.argmax(pred[:, :, -1], dim=1, keepdim=True),
                    ],
                    dim=1,
                )
                reached_end = torch.logical_or(
                    reached_end,
                    torch.eq(predicted_tokens[:, -1], self.dataset.tokens["end"]),
                )
                predicted_tokens_len += 1

                prediction_len[reached_end == False] = i + 1  # noqa E712
                if torch.all(reached_end):
                    break

            confidence_scores = (
                torch.cat(confidence_scores, dim=1).cpu().detach().numpy()
            )
            predicted_tokens = predicted_tokens[:, 1:]
            prediction_len[torch.eq(reached_end, False)] = max_chars - 1
            predicted_tokens = [
                predicted_tokens[i, : prediction_len[i]] for i in range(b)
            ]
            confidence_scores = [
                confidence_scores[i, : prediction_len[i]].tolist() for i in range(b)
            ]
            str_x = [
                ind_to_token(self.dataset.charset, t, oov_symbol="")
                for t in predicted_tokens
            ]

        process_time = time() - start_time

        values = {
            "nb_samples": b,
            "str_y": batch_data["raw_labels"],
            "str_x": str_x,
            "confidence_score": confidence_scores,
            "time": process_time,
        }
        if self.lm_decoder:
            values["str_lm"] = self.lm_decoder(tot_pred, prediction_len)["text"]

        return values
