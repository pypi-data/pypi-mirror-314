# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import json
import logging
import random
from collections import defaultdict
from pathlib import Path
from typing import Dict, List
from uuid import UUID

from tqdm import tqdm

from arkindex_export import Dataset, DatasetElement, Element, open_database
from dan.datasets.extract.db import (
    get_dataset_elements,
    get_elements,
    get_transcription_entities,
    get_transcriptions,
)
from dan.datasets.extract.exceptions import (
    NoTranscriptionError,
    ProcessingError,
)
from dan.datasets.extract.utils import (
    entities_to_xml,
    get_translation_map,
    normalize_linebreaks,
    normalize_spaces,
)
from dan.utils import parse_tokens

TRAIN_NAME = "train"
VAL_NAME = "val"
TEST_NAME = "test"
SPLIT_NAMES = [TRAIN_NAME, VAL_NAME, TEST_NAME]

logger = logging.getLogger(__name__)


class ArkindexExtractor:
    """
    Extract data from Arkindex
    """

    def __init__(
        self,
        output: Path,
        dataset_ids: List[UUID] | None = None,
        element_type: List[str] = [],
        entity_separators: List[str] = ["\n", " "],
        tokens: Path | None = None,
        transcription_worker_versions: List[str | bool] = [],
        entity_worker_versions: List[str | bool] = [],
        transcription_worker_runs: List[str | bool] = [],
        entity_worker_runs: List[str | bool] = [],
        keep_spaces: bool = False,
        allow_empty: bool = False,
    ) -> None:
        self.dataset_ids = dataset_ids
        self.element_type = element_type
        self.output = output
        self.entity_separators = entity_separators
        self.tokens = parse_tokens(tokens) if tokens else {}
        self.transcription_worker_versions = transcription_worker_versions
        self.entity_worker_versions = entity_worker_versions
        self.transcription_worker_runs = transcription_worker_runs
        self.entity_worker_runs = entity_worker_runs
        self.allow_empty = allow_empty
        self.keep_spaces = keep_spaces

        data_path = self.output / "split.json"
        # New keys can appear between several extractions
        # We must explicitly define that this dict expects a dict as its value
        self.data = defaultdict(dict)
        if data_path.exists():
            self.data.update(json.loads(data_path.read_text()))

        # NER extraction
        self.translation_map: Dict[str, str] | None = get_translation_map(self.tokens)

    def translate(self, text: str):
        """
        Use translation map to replace XML tags to actual tokens
        """
        for pattern, repl in self.translation_map.items():
            text = text.replace(pattern, repl)
        return text

    def extract_transcription(self, element: Element):
        """
        Extract the element's transcription.
        If the entities are needed, they are added to the transcription using tokens.
        """
        transcriptions = get_transcriptions(
            element.id,
            self.transcription_worker_versions,
            self.transcription_worker_runs,
        )
        if len(transcriptions) == 0:
            if self.allow_empty:
                return ""
            raise NoTranscriptionError(element.id)

        transcription = random.choice(transcriptions)
        stripped_text = transcription.text.strip()

        if not self.tokens:
            return stripped_text

        entities = get_transcription_entities(
            transcription.id,
            self.entity_worker_versions,
            self.entity_worker_runs,
            supported_types=list(self.tokens),
        )

        if not entities.count():
            return stripped_text

        return self.translate(
            entities_to_xml(
                transcription.text, entities, entity_separators=self.entity_separators
            )
        )

    def format_text(self, text: str):
        if not self.keep_spaces:
            text = normalize_spaces(text)
            text = normalize_linebreaks(text)

        return text.strip()

    def process_element(self, dataset_parent: DatasetElement, element: Element):
        """
        Extract an element's data and save it to disk.
        The output path is directly related to the split of the element.
        """
        text = self.extract_transcription(element)
        text = self.format_text(text)

        self.data[dataset_parent.set_name][element.id] = {
            "dataset_id": dataset_parent.dataset_id,
            "text": text,
            "image": {
                "iiif_url": element.image.url,
                "polygon": json.loads(element.polygon),
            },
        }

    def process_parent(self, pbar, dataset_parent: DatasetElement):
        """
        Extract data from a parent element.
        """
        parent = dataset_parent.element
        base_description = f"Extracting data from {parent.type} ({parent.id}) for split ({dataset_parent.set_name})"
        pbar.set_description(desc=base_description)
        if self.element_type == [parent.type]:
            try:
                self.process_element(dataset_parent, parent)
            except ProcessingError as e:
                logger.warning(f"Skipping {parent.id}: {str(e)}")
        # Extract children elements
        else:
            children = get_elements(
                parent.id,
                self.element_type,
            )

            nb_children = children.count()
            for idx, element in enumerate(children, start=1):
                # Update description to update the children processing progress
                pbar.set_description(desc=base_description + f" ({idx}/{nb_children})")
                try:
                    self.process_element(dataset_parent, element)
                except ProcessingError as e:
                    logger.warning(f"Skipping {element.id}: {str(e)}")

    def export(self):
        (self.output / "split.json").write_text(
            json.dumps(
                self.data,
                sort_keys=True,
                indent=4,
            )
        )

    def run(self):
        # Retrieve the Dataset and its splits from the cache
        for dataset_id in self.dataset_ids:
            dataset = Dataset.get_by_id(dataset_id)
            splits = dataset.sets.split(",")
            if not set(splits).issubset(set(SPLIT_NAMES)):
                logger.warning(
                    f'Dataset {dataset.name} ({dataset.id}) does not have "{TRAIN_NAME}", "{VAL_NAME}" and "{TEST_NAME}" steps'
                )
                continue

            # Extract the train set first to correctly build the `self.charset` variable
            splits.remove(TRAIN_NAME)
            splits.insert(0, TRAIN_NAME)

            # Iterate over the subsets to find the page images and labels.
            for split in splits:
                with tqdm(
                    get_dataset_elements(dataset, split),
                    desc=f"Extracting data from ({dataset_id}) for split ({split})",
                ) as pbar:
                    # Iterate over the pages to create splits at page level.
                    for parent in pbar:
                        self.process_parent(
                            pbar=pbar,
                            dataset_parent=parent,
                        )
                        # Progress bar updates
                        pbar.update()
                        pbar.refresh()

        if not self.data:
            raise Exception(
                "No data was extracted using the provided export database and parameters."
            )

        self.export()


def run(
    database: Path,
    dataset_ids: List[UUID],
    element_type: List[str],
    output: Path,
    entity_separators: List[str],
    tokens: Path,
    transcription_worker_versions: List[str | bool],
    entity_worker_versions: List[str | bool],
    transcription_worker_runs: List[str | bool],
    entity_worker_runs: List[str | bool],
    keep_spaces: bool,
    allow_empty: bool,
):
    assert database.exists(), f"No file found @ {database}"
    open_database(path=database)

    # Create directories
    output.mkdir(parents=True, exist_ok=True)

    ArkindexExtractor(
        dataset_ids=dataset_ids,
        element_type=element_type,
        output=output,
        entity_separators=entity_separators,
        tokens=tokens,
        transcription_worker_versions=transcription_worker_versions,
        entity_worker_versions=entity_worker_versions,
        transcription_worker_runs=transcription_worker_runs,
        entity_worker_runs=entity_worker_runs,
        keep_spaces=keep_spaces,
        allow_empty=allow_empty,
    ).run()
