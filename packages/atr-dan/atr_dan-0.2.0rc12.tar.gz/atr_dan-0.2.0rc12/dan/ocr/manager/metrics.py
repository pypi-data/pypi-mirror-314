# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import re
from collections import defaultdict
from operator import attrgetter
from pathlib import Path
from typing import Dict, List, NamedTuple

import editdistance
import numpy as np

from dan.utils import parse_tokens

# Remove punctuation
REGEX_PUNCTUATION = re.compile(r"([\[\]{}/\\()\"'&+*=<>?.;:,!\-—_€#%°])")
# Remove consecutive linebreaks
REGEX_CONSECUTIVE_LINEBREAKS = re.compile(r"\n+")
# Remove consecutive spaces
REGEX_CONSECUTIVE_SPACES = re.compile(r" +")
# Keep only one space character
REGEX_ONLY_ONE_SPACE = re.compile(r"\s+")

# Mapping between computation tasks (CER, WER, NER) and their metric keyword
METRICS_KEYWORD = {"cer": "chars", "wer": "words", "ner": "tokens"}


class Inference(NamedTuple):
    """
    Store a prediction with its ground truth to avoid
    inferring again when we need to compute new metrics
    """

    image: str
    ground_truth: str
    prediction: str
    lm_prediction: str
    wer: float


class MetricManager:
    def __init__(self, metric_names: List[str], dataset_name: str, tokens: Path | None):
        self.dataset_name: str = dataset_name
        self.remove_tokens: str = None

        if tokens:
            tokens = parse_tokens(tokens)
            layout_tokens = "".join(
                list(map(attrgetter("start"), tokens.values()))
                + list(map(attrgetter("end"), tokens.values()))
            )
            self.remove_tokens: re.Pattern = re.compile(r"([" + layout_tokens + "])")
            self.keep_tokens: re.Pattern = re.compile(r"([^" + layout_tokens + "])")

        self.metric_names: List[str] = metric_names
        self.epoch_metrics = defaultdict(list)

    def format_string_for_cer(self, text: str, remove_token: bool = False):
        """
        Format string for CER computation: remove layout tokens and extra spaces
        """
        if remove_token and self.remove_tokens is not None:
            text = self.remove_tokens.sub("", text)

        text = REGEX_CONSECUTIVE_LINEBREAKS.sub("\n", text)
        return REGEX_CONSECUTIVE_SPACES.sub(" ", text).strip()

    def format_string_for_wer(
        self, text: str, remove_punct: bool = False, remove_token: bool = False
    ):
        """
        Format string for WER computation: remove layout tokens, treat punctuation as word, replace line break by space
        """
        if remove_punct:
            text = REGEX_PUNCTUATION.sub("", text)
        if remove_token and self.remove_tokens is not None:
            text = self.remove_tokens.sub("", text)
        return REGEX_ONLY_ONE_SPACE.sub(" ", text).strip().split(" ")

    def format_string_for_ner(self, text: str):
        """
        Format string for NER computation: only keep layout tokens
        """
        return self.keep_tokens.sub("", text)

    def _format_string(self, task: str, *args, **kwargs):
        """
        Call the proper `format_string_for_*` method for the given task
        """
        match task:
            case "cer":
                return self.format_string_for_cer(*args, **kwargs)
            case "wer":
                return self.format_string_for_wer(*args, **kwargs)
            case "ner":
                return self.format_string_for_ner(*args, **kwargs)

    def update_metrics(self, batch_metrics):
        """
        Add batch metrics to the metrics
        """
        for key in batch_metrics:
            self.epoch_metrics[key] += batch_metrics[key]

    def get_display_values(self, output: bool = False):
        """
        Format metrics values for shell display purposes
        """
        metric_names = self.metric_names.copy()
        if output:
            metric_names.append("nb_samples")
        display_values = dict()
        for metric_name in metric_names:
            match metric_name:
                case "time" | "nb_samples":
                    if not output:
                        continue
                    value = int(np.sum(self.epoch_metrics[metric_name]))
                    if metric_name == "time":
                        sample_time = value / np.sum(self.epoch_metrics["nb_samples"])
                        display_values["sample_time"] = float(round(sample_time, 4))
                    display_values[metric_name] = value
                    continue
                case (
                    "cer"
                    | "cer_no_token"
                    | "wer"
                    | "wer_no_punct"
                    | "wer_no_token"
                    | "ner"
                ):
                    keyword = METRICS_KEYWORD[metric_name[:3]]
                    suffix = metric_name[3:]
                    num_name, denom_name = (
                        "edit_" + keyword + suffix,
                        "nb_" + keyword + suffix,
                    )
                case "loss" | "loss_ce":
                    display_values[metric_name] = round(
                        float(
                            np.average(
                                self.epoch_metrics[metric_name],
                                weights=np.array(self.epoch_metrics["nb_samples"]),
                            ),
                        ),
                        4,
                    )
                    continue
                case _:
                    continue

            value = float(
                np.sum(self.epoch_metrics[num_name])
                / np.sum(self.epoch_metrics[denom_name])
            )
            if output:
                display_values[denom_name] = int(np.sum(self.epoch_metrics[denom_name]))
            display_values[metric_name] = round(value, 4)
        return display_values

    def compute_metrics(
        self, values: Dict[str, int | float], metric_names: List[str]
    ) -> Dict[str, List[int | float]]:
        metrics = {
            "nb_samples": [
                values["nb_samples"],
            ],
        }
        if "time" in values:
            metrics["time"] = [values["time"]]

        gt, prediction = values["str_y"], values["str_x"]
        for metric_name in metric_names:
            match metric_name:
                case (
                    "cer"
                    | "cer_no_token"
                    | "wer"
                    | "wer_no_punct"
                    | "wer_no_token"
                    | "ner"
                ):
                    task = metric_name[:3]
                    keyword = METRICS_KEYWORD[task]
                    suffix = metric_name[3:]

                    # Add extra parameters for the format functions
                    extras = []
                    if suffix == "_no_punct":
                        extras.append([{"remove_punct": True}])
                    elif suffix == "_no_token":
                        extras.append([{"remove_token": True}])

                    # Run the format function for the desired computation (CER, WER or NER)
                    split_gt = list(map(self._format_string, [task], gt, *extras))
                    split_pred = list(
                        map(self._format_string, [task], prediction, *extras)
                    )

                    # Compute and store edit distance/length for the desired level
                    # (chars, words or tokens) as metrics
                    metrics["edit_" + keyword + suffix] = list(
                        map(editdistance.eval, split_gt, split_pred)
                    )
                    metrics["nb_" + keyword + suffix] = list(map(len, split_gt))
                    metrics[keyword + "_error_rate" + suffix] = [
                        round(float(edit_dist / gt_len), 4)
                        if gt_len
                        else float(bool(edit_dist))
                        for edit_dist, gt_len in zip(
                            metrics["edit_" + keyword + suffix],
                            metrics["nb_" + keyword + suffix],
                        )
                    ]
                case "loss" | "loss_ce":
                    metrics[metric_name] = [
                        values[metric_name],
                    ]
        return metrics

    def get(self, name: str):
        return self.epoch_metrics[name]
