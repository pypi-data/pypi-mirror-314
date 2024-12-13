# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

"""
Convert DAN predictions to BIO format.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, List

from tqdm import tqdm

from dan.utils import EntityType, parse_tokens

logger = logging.getLogger(__name__)


def add_convert_bio_parser(subcommands):
    parser = subcommands.add_parser(
        "convert",
        description=__doc__,
        help=__doc__,
    )
    parser.set_defaults(func=run)

    parser.add_argument(
        "predictions",
        type=Path,
        help="Path to a folder of DAN predictions.",
    )

    parser.add_argument(
        "--tokens",
        type=Path,
        help="Mapping between starting tokens and end tokens to extract text with their entities.",
        required=True,
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Where BIO files are saved. Will be created if missing.",
        required=True,
    )


def convert(text: str, ner_tokens: Dict[str, EntityType]) -> str:
    # Mapping to find a starting token for an ending token efficiently
    mapping_end_start: Dict[str, str] = {
        entity_type.end: entity_type.start for entity_type in ner_tokens.values()
    }
    # Mapping to find the entity name for a starting token efficiently
    mapping_start_name: Dict[str, str] = {
        entity_type.start: name for name, entity_type in ner_tokens.items()
    }

    starting_tokens: List[str] = mapping_start_name.keys()
    ending_tokens: List[str] = mapping_end_start.keys()
    has_ending_tokens: bool = set(ending_tokens) != {
        ""
    }  # Whether ending tokens are used

    # Spacing starting tokens and ending tokens (if necessary)
    tokens_spacing: re.Pattern = re.compile(
        r"([" + "".join([*starting_tokens, *ending_tokens]) + "])"
    )
    text: str = tokens_spacing.sub(r" \1 ", text)

    iob: List[str] = []  # List of IOB formatted strings
    entity_types: List[str] = []  # Encountered entity types
    inside: bool = False  # Whether we are inside an entity
    for token in text.split():
        # Encountering a starting token
        if token in starting_tokens:
            entity_types.append(token)

            # Stopping any current entity type
            inside = False

            continue

        # Encountering an ending token
        elif has_ending_tokens and token in ending_tokens:
            if not entity_types:
                logger.warning(
                    f"Missing starting token for ending token {token}, skipping the entity"
                )
                continue

            # Making sure this ending token closes the current entity
            assert (
                entity_types[-1] == mapping_end_start[token]
            ), f"Ending token {token} doesn't match the starting token {entity_types[-1]}"

            # Removing the current entity from the queue as it is its end
            entity_types.pop()

            # If there is still entities in the queue, we continue in the parent one
            # Else, we are not in any entity anymore
            inside = bool(entity_types)

            continue

        # The token is not part of an entity
        if not entity_types:
            iob.append(f"{token} O")
            continue

        # The token is part of at least one entity
        entity_name: str = mapping_start_name[entity_types[-1]]

        if inside:
            # Inside the same entity
            iob.append(f"{token} I-{entity_name}")
            continue

        # Starting a new entity
        iob.append(f"{token} B-{entity_name}")
        inside = True

    # Concatenating all formatted iob strings
    return "\n".join(iob)


def run(
    predictions: Path,
    tokens: Path,
    output: Path,
):
    # Create output folder
    output.mkdir(parents=True, exist_ok=True)

    # Load tokens
    ner_tokens = parse_tokens(tokens)

    for prediction in tqdm(
        list(predictions.glob("*.json")), desc="Converting predictions"
    ):
        data = json.loads(prediction.read_text())
        try:
            bio_representation = convert(data["text"], ner_tokens)
        except Exception as e:
            logger.error(f"Failed to convert {prediction.name}: {e}")
            continue

        (output / prediction.stem).with_suffix(".bio").write_text(bio_representation)
