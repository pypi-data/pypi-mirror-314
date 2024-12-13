# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import json
import re
from argparse import ArgumentTypeError
from itertools import islice, takewhile
from operator import attrgetter
from pathlib import Path
from typing import Dict, NamedTuple

import torch
import torchvision.io as torchvision
import yaml


class MLflowNotInstalled(Exception):
    """
    Raised when MLflow logging was requested but the module was not installed
    """


class Token(NamedTuple):
    encoded: str
    display: str


class LMTokenMapping(NamedTuple):
    space: Token = Token("▁", " ")
    linebreak: Token = Token("↵", "\n")
    ctc: Token = Token("◌", "<ctc>")

    @property
    def display(self):
        return {a.encoded: a.display for a in self}

    @property
    def encode(self):
        return {a.display: a.encoded for a in self}

    def encode_token(self, token: str) -> str:
        return self.encode.get(token, token)


class EntityType(NamedTuple):
    start: str
    end: str = ""

    @property
    def offset(self):
        return len(self.start) + len(self.end)


def pad_sequences_1D(data, padding_value):
    """
    Pad data with padding_value to get same length
    """
    x_lengths = [len(x) for x in data]
    longest_x = max(x_lengths)
    padded_data = torch.ones((len(data), longest_x), dtype=torch.int32) * padding_value
    for i, x_len in enumerate(x_lengths):
        padded_data[i, :x_len] = torch.tensor(data[i][:x_len])
    return padded_data


def pad_images(images):
    """
    Pad the images so that they are at the top left of the large padded image.
    :param images: List of images as torch tensors.
    :return padded_images: A tensor containing all the padded images.
    """
    longest_x = max([x.shape[1] for x in images])
    longest_y = max([x.shape[2] for x in images])
    padded_images = torch.zeros((len(images), images[0].shape[0], longest_x, longest_y))
    for index, image in enumerate(images):
        padded_images[
            index,
            :,
            0 : image.shape[1],
            0 : image.shape[2],
        ] = image
    return padded_images


def read_image(path: str):
    """
    Read image with torch
    :param path: Path of the image to load.
    """
    img = torchvision.read_image(path, mode=torchvision.ImageReadMode.RGB)
    return img.to(dtype=torch.get_default_dtype()).div(255)


# Charset / labels conversion
def token_to_ind(labels, str):
    return [labels.index(c) for c in str]


def ind_to_token(labels, ind, oov_symbol=None):
    if oov_symbol is not None:
        res = []
        for i in ind:
            if i < len(labels):
                res.append(labels[i])
            else:
                res.append(oov_symbol)
    else:
        res = [labels[i] for i in ind]
    return "".join(res)


def fix_ddp_layers_names(model, to_ddp):
    """
    Rename the model layers if they were saved using DDP or if they will
    be used with DDP.
    :param model: Model to update.
    :param to_ddp: Convert layers names to be used by DDP.
    :return: The model with corrected layers names.
    """
    if to_ddp:
        return {
            ("module." + k if "module" not in k else k): v for k, v in model.items()
        }
    return {k.replace("module.", ""): v for k, v in model.items()}


def list_to_batches(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # list_to_batches('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def parse_tokens(filename: str) -> Dict[str, EntityType]:
    tokens = {
        name: EntityType(**tokens)
        for name, tokens in yaml.safe_load(Path(filename).read_text()).items()
    }
    end_tokens = map(attrgetter("end"), tokens.values())
    # Check that either
    if next(end_tokens):
        # - all entities have end token
        assert all(end_tokens), "Some entities have no end token"
    else:
        # - no entities have end tokens
        assert not any(end_tokens), "Some entities have end tokens"

    return tokens


def parse_tokens_pattern(tokens: list[EntityType]) -> re.Pattern[str]:
    starting_tokens = "".join(token.start for token in tokens)
    # Check if there are end tokens
    if all(token.end for token in tokens):
        # Matches a starting token, the corresponding ending token, and any text in between
        return re.compile(
            r"|".join(f"({token.start}.*?{token.end})" for token in tokens)
        )

    # Matches a starting token then any character that is not a starting token
    return re.compile(rf"([{starting_tokens}][^{starting_tokens}]*)")


def parse_charset_pattern(charset: list[str]) -> re.Pattern[str]:
    """
    Use (...) for tokens with a longer length than 1, otherwise, use [...].
    Longer words are matched first by the pattern.
    """

    tokens = sorted(charset, key=len)

    # 1 character length
    letters = list(takewhile(lambda t: len(t) == 1, tokens))

    pattern = ""

    if words := tokens[len(letters) :]:
        # More than 1 character length
        # (?:...)|(?:...)...
        # Create non capturing groups to be able to split with re.findall
        pattern += (
            r"|".join(f"(?:{re.escape(token)})" for token in reversed(words)) + "|"
        )

    # [...] used for 1-length tokens
    pattern += "[" + r"".join(map(re.escape, letters)) + "]"

    return re.compile(pattern)


def read_yaml(yaml_path: str) -> Dict:
    """
    Read YAML tokens file.
    :param yaml_path: Path of the YAML file to read.
    :return: The content of the read file.
    """
    filename = Path(yaml_path)
    assert filename.exists(), f"{yaml_path} does not resolve."
    try:
        return yaml.safe_load(filename.read_text())
    except yaml.YAMLError as e:
        raise ArgumentTypeError(e)


def read_json(json_path: str) -> Dict:
    """
    Read labels JSON file
    :param json_path: Path of the JSON file to read.
    :return: The content of the read file.
    """
    filename = Path(json_path)
    assert filename.exists(), f"{json_path} does not resolve."
    try:
        return json.loads(filename.read_text())
    except json.JSONDecodeError as e:
        raise ArgumentTypeError(e)


def read_txt(txt_path: str) -> str:
    """
    Read TXT file.
    :param txt_path: Path of the text file to read.
    :return: The content of the read file.
    """
    filename = Path(txt_path)
    assert filename.exists(), f"{txt_path} does not resolve."
    return filename.read_text()
