# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

from operator import itemgetter

import pytest

from arkindex_export import Dataset, DatasetElement, Element
from dan.datasets.extract.arkindex import TRAIN_NAME
from dan.datasets.extract.db import (
    get_dataset_elements,
    get_elements,
    get_transcription_entities,
    get_transcriptions,
)


def test_get_dataset_elements(mock_database):
    """
    Assert dataset elements retrieval output against verified results
    """
    dataset_elements = get_dataset_elements(
        dataset=Dataset.select().get(),
        split=TRAIN_NAME,
    )

    # ID verification
    assert all(
        isinstance(dataset_element, DatasetElement)
        for dataset_element in dataset_elements
    )
    assert [dataset_element.element.id for dataset_element in dataset_elements] == [
        "train-page_1",
        "train-page_2",
    ]


def test_get_elements(mock_database):
    """
    Assert elements retrieval output against verified results
    """
    elements = get_elements(
        parent_id="train-page_1",
        element_type=["text_line"],
    )

    # ID verification
    assert all(isinstance(element, Element) for element in elements)
    assert [element.id for element in elements] == [
        "train-page_1-line_1",
        "train-page_1-line_2",
        "train-page_1-line_3",
        "train-page_1-line_4",
    ]


@pytest.mark.parametrize(
    "sources",
    ([False], ["id"], [], [False, "id"]),
)
def test_get_transcriptions(sources, mock_database):
    """
    Assert transcriptions retrieval output against verified results
    """
    worker_versions = [
        f"worker_version_{source}" if isinstance(source, str) else source
        for source in sources
    ]
    worker_runs = [
        f"worker_run_{source}" if isinstance(source, str) else source
        for source in sources
    ]

    element_id = "train-page_1-line_1"
    transcriptions = get_transcriptions(
        element_id=element_id,
        transcription_worker_versions=worker_versions,
        transcription_worker_runs=worker_runs,
    )

    expected_transcriptions = []
    if not sources or False in sources:
        expected_transcriptions.append(
            {
                "text": "Laulont  Francois  8",
                "worker_version": None,
                "worker_run": None,
            }
        )

    if not sources or "id" in sources:
        expected_transcriptions.append(
            {
                "text": "laulont  francois  8",
                "worker_version": "worker_version_id",
                "worker_run": "worker_run_id",
            }
        )

    # Do not compare IDs
    transcriptions = transcriptions.dicts()
    for transcription in transcriptions:
        del transcription["id"]

    assert sorted(transcriptions, key=itemgetter("text")) == expected_transcriptions


@pytest.mark.parametrize("source", (False, "id", None))
@pytest.mark.parametrize(
    "supported_types", (["surname"], ["surname", "firstname", "age"])
)
def test_get_transcription_entities(source, mock_database, supported_types):
    worker_version = f"worker_version_{source}" if isinstance(source, str) else source
    worker_run = f"worker_run_{source}" if isinstance(source, str) else source

    transcription_id = "train-page_1-line_1" + ("source" if source else "")
    entities = get_transcription_entities(
        transcription_id=transcription_id,
        entity_worker_versions=[worker_version] if worker_version is not None else [],
        entity_worker_runs=[worker_run] if worker_run is not None else [],
        supported_types=supported_types,
    )

    expected_entities = [
        {
            "name": "Laulont",
            "type": "surname",
            "offset": 0,
            "length": 7,
        },
        {
            "name": "Francois",
            "type": "firstname",
            "offset": 9,
            "length": 8,
        },
        {
            "name": "8",
            "type": "age",
            "offset": 19,
            "length": 1,
        },
    ]

    expected_entities = list(
        filter(lambda ent: ent["type"] in supported_types, expected_entities)
    )
    for entity in expected_entities:
        if source:
            entity["name"] = entity["name"].lower()
        entity["worker_version"] = worker_version or None
        entity["worker_run"] = worker_run or None

    assert sorted(entities, key=itemgetter("offset")) == expected_entities
