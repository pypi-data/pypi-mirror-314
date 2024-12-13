# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import re
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "data"

TWO_SPACES_REGEX = re.compile(r" {2}")


def change_split_content(
    load_entities: bool,
    transcription_entities_worker_version: str | bool,
    keep_spaces: bool,
    split_content: dict,
    tokens: list,
    expected_labels: dict = [],
):
    # Transcriptions with worker version are in lowercase
    if transcription_entities_worker_version:
        for split in split_content:
            for element_id in split_content[split]:
                split_content[split][element_id]["text"] = split_content[split][
                    element_id
                ]["text"].lower()
        for split in expected_labels:
            for image in expected_labels[split]:
                expected_labels[split][image] = expected_labels[split][image].lower()

    # If we do not load entities, remove tokens
    if not load_entities:
        token_translations = {ord(token): None for token in tokens}
        for split in split_content:
            for element_id in split_content[split]:
                split_content[split][element_id]["text"] = split_content[split][
                    element_id
                ]["text"].translate(token_translations)
        for split in expected_labels:
            for image in expected_labels[split]:
                expected_labels[split][image] = expected_labels[split][image].translate(
                    token_translations
                )

    # Replace double spaces with regular space
    if not keep_spaces:
        for split in split_content:
            for element_id in split_content[split]:
                split_content[split][element_id]["text"] = TWO_SPACES_REGEX.sub(
                    " ", split_content[split][element_id]["text"]
                )
        for split in expected_labels:
            for image in expected_labels[split]:
                expected_labels[split][image] = TWO_SPACES_REGEX.sub(
                    " ", expected_labels[split][image]
                )

    return split_content, expected_labels
