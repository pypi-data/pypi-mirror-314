# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import json
import uuid
from operator import itemgetter
from typing import List

import pytest

from arkindex_export import (
    Dataset,
    DatasetElement,
    Element,
    ElementPath,
    Entity,
    EntityType,
    Image,
    ImageServer,
    Transcription,
    TranscriptionEntity,
    WorkerRun,
    WorkerVersion,
    database,
)
from dan.datasets.extract.arkindex import TEST_NAME, TRAIN_NAME, VAL_NAME
from tests import FIXTURES


@pytest.fixture()
def mock_database(tmp_path_factory):
    def create_transcription_entity(
        transcription: Transcription,
        worker_version: str | None,
        worker_run: str | None,
        type: str,
        name: str,
        offset: int,
    ) -> None:
        entity_type, _ = EntityType.get_or_create(
            name=type, defaults={"id": f"{type}_id"}
        )
        entity = Entity.create(
            id=str(uuid.uuid4()),
            name=name,
            type=entity_type,
            worker_version=worker_version,
            worker_run=worker_run,
        )
        TranscriptionEntity.create(
            id=str(uuid.uuid4()),
            entity=entity,
            length=len(name),
            offset=offset,
            transcription=transcription,
            worker_version=worker_version,
            worker_run=worker_run,
        )

    def create_transcriptions(element: Element, entities: List[dict]) -> None:
        if not entities:
            return

        # Add transcription with entities
        entities = sorted(entities, key=itemgetter("offset"))

        # We will add extra spaces to test the "keep_spaces" parameters of the "extract" command
        for offset, entity in enumerate(entities[1:], start=1):
            entity["offset"] += offset

        for worker_version, worker_run in [
            (None, None),
            ("worker_version_id", "worker_run_id"),
        ]:
            transcription_suffix = ""
            # Use different transcriptions to filter by worker version
            if worker_version and worker_run:
                transcription_suffix = "source"
                for entity in entities:
                    entity["name"] = entity["name"].lower()

            transcription = Transcription.create(
                id=element.id + transcription_suffix,
                # Add extra spaces to test the "keep_spaces" parameters of the "extract" command
                text="  ".join(map(itemgetter("name"), entities)),
                element=element,
                worker_version=worker_version,
                worker_run=worker_run,
            )

            for entity in entities:
                create_transcription_entity(
                    transcription=transcription,
                    worker_version=worker_version,
                    worker_run=worker_run,
                    **entity,
                )

    def create_element(id: str, parent: Element | None = None) -> None:
        element_path = (FIXTURES / "extraction" / "elements" / id).with_suffix(".json")
        element_json = json.loads(element_path.read_text())

        element_type = element_json["type"]
        image_path = (FIXTURES / "extraction" / "images" / id).with_suffix(".jpg")

        polygon = element_json.get("polygon")
        # Always use page images because polygons are based on the full image
        image, _ = (
            Image.get_or_create(
                id=id + "-image",
                defaults={
                    "server": image_server,
                    # Use path to image instead of actual URL since we won't be doing any download
                    "url": image_path,
                    "width": 0,
                    "height": 0,
                },
            )
            if polygon
            else (None, False)
        )

        element = Element.create(
            id=id,
            name=id,
            type=element_type,
            image=image,
            polygon=json.dumps(polygon) if polygon else None,
            created=0.0,
            updated=0.0,
        )

        if parent:
            ElementPath.create(id=str(uuid.uuid4()), parent=parent, child=element)

        create_transcriptions(
            element=element,
            entities=element_json.get("transcription_entities", []),
        )

        # Recursive function to create children
        for child in element_json.get("children", []):
            create_element(id=child, parent=element)

    MODELS = [
        WorkerVersion,
        WorkerRun,
        ImageServer,
        Image,
        Dataset,
        DatasetElement,
        Element,
        ElementPath,
        EntityType,
        Entity,
        Transcription,
        TranscriptionEntity,
    ]

    # Initialisation
    tmp_path = tmp_path_factory.mktemp("data")
    database_path = tmp_path / "db.sqlite"
    database.init(
        database_path,
        pragmas={
            # Recommended settings from peewee
            # http://docs.peewee-orm.com/en/latest/peewee/database.html#recommended-settings
            # Do not set journal mode to WAL as it writes in the database
            "cache_size": -1 * 64000,  # 64MB
            "foreign_keys": 1,
            "ignore_check_constraints": 0,
            "synchronous": 0,
        },
    )
    database.connect()

    # Create tables
    database.create_tables(MODELS)

    image_server = ImageServer.create(
        url="http://image/server/url",
        display_name="Image server",
    )

    WorkerVersion.create(
        id="worker_version_id",
        slug="worker_version",
        name="Worker version",
        repository_url="http://repository/url",
        revision="main",
        type="worker",
    )

    WorkerRun.create(
        id="worker_run_id",
        worker_version="worker_version_id",
    )

    # Create dataset
    split_names = [VAL_NAME, TEST_NAME, TRAIN_NAME]
    dataset = Dataset.create(
        id="dataset_id",
        name="Dataset",
        state="complete",
        sets=",".join(split_names),
        description="My Dataset",
    )

    # Create dataset elements
    for split in split_names:
        element_path = (FIXTURES / "extraction" / "elements" / split).with_suffix(
            ".json"
        )
        element_json = json.loads(element_path.read_text())

        # Recursive function to create children
        for child in element_json.get("children", []):
            create_element(id=child)

            # Linking the element to the dataset split
            DatasetElement.create(
                id=child, element_id=child, dataset=dataset, set_name=split
            )

    # Create data for entities extraction tests
    # Create transcription
    transcription = Transcription.create(
        id="tr-with-entities",
        text="The great king Charles III has eaten \nwith us.",
        element=Element.select().first(),
    )

    # Create worker version and worker run
    for nestation in ("nested", "non-nested", "special-chars"):
        WorkerVersion.create(
            id=f"worker-version-{nestation}-id",
            slug=nestation,
            name=nestation,
            repository_url="http://repository/url",
            revision="main",
            type="worker",
        )
        WorkerRun.create(
            id=f"worker-run-{nestation}-id",
            worker_version=f"worker-version-{nestation}-id",
        )

    # Create entities
    for entity in [
        # Non-nested entities
        {
            "source": "non-nested",
            "type": "adj",
            "name": "great",
            "offset": 4,
        },
        {
            "source": "non-nested",
            "type": "name",
            "name": "Charles",
            "offset": 15,
        },
        {
            "source": "non-nested",
            "type": "person",
            "name": "us",
            "offset": 43,
        },
        # Nested entities
        {
            "source": "nested",
            "type": "fullname",
            "name": "Charles III",
            "offset": 15,
        },
        {
            "source": "nested",
            "type": "name",
            "name": "Charles",
            "offset": 15,
        },
        {
            "source": "nested",
            "type": "person",
            "name": "us",
            "offset": 43,
        },
        # Special characters
        {
            "source": "special-chars",
            "type": "Arkindex's entity",
            "name": "great",
            "offset": 4,
        },
        {
            "source": "special-chars",
            "type": '"Name" (1)',
            "name": "Charles",
            "offset": 15,
        },
        {
            "source": "special-chars",
            "type": "Person /!\\",
            "name": "us",
            "offset": 43,
        },
    ]:
        source = entity.pop("source")
        create_transcription_entity(
            transcription=transcription,
            worker_version=f"worker-version-{source}-id",
            worker_run=f"worker-run-{source}-id",
            **entity,
        )

    return database_path


@pytest.fixture
def training_config():
    return json.loads((FIXTURES.parent.parent / "configs" / "tests.json").read_text())


@pytest.fixture
def evaluate_config():
    return json.loads((FIXTURES.parent.parent / "configs" / "eval.json").read_text())


@pytest.fixture
def split_content():
    splits = json.loads((FIXTURES / "extraction" / "split.json").read_text())
    for split in splits:
        for element_id in splits[split]:
            splits[split][element_id]["image"]["iiif_url"] = splits[split][element_id][
                "image"
            ]["iiif_url"].replace("{FIXTURES}", str(FIXTURES))

    return splits
