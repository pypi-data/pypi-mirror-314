# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Iterable

import yaml

OFFSET = 86
LIMIT = 160

STARTING_TOKEN = "\u2460"


def get_token() -> Iterable[str]:
    offset = OFFSET

    while offset < LIMIT:
        yield chr(ord(STARTING_TOKEN) + offset % LIMIT)
        offset += 1

    raise Exception(f"More than {LIMIT} tokens asked")


def run(entities: Path, end_tokens: bool, output_file: Path) -> None:
    # Load extracted entities
    entities = yaml.safe_load(entities.read_text())

    # Generate associated starting/ending token
    token_generator = get_token()
    tokens = {}
    for entity in entities.get("entities", []):
        tokens[entity] = {
            "start": next(token_generator),
            "end": next(token_generator) if end_tokens else "",
        }

    # Save entities & tokens to YAML
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(
        yaml.safe_dump(tokens, explicit_start=True, allow_unicode=True, sort_keys=False)
    )
