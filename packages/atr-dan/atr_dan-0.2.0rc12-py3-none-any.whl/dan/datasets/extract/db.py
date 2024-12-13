# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
from typing import List

from peewee import JOIN

from arkindex_export import Image, WorkerRun
from arkindex_export.models import (
    Dataset,
    DatasetElement,
    Element,
    Entity,
    EntityType,
    Transcription,
    TranscriptionEntity,
)
from arkindex_export.queries import list_children


def get_dataset_elements(
    dataset: Dataset,
    split: str,
):
    """
    Retrieve dataset elements in a specific split from an SQLite export of an Arkindex corpus
    """
    query = (
        DatasetElement.select()
        .join(Element)
        .join(Image, on=(DatasetElement.element.image == Image.id))
        .where(
            DatasetElement.dataset == dataset,
            DatasetElement.set_name == split,
        )
    )

    return query


def get_elements(
    parent_id: str,
    element_type: List[str],
):
    """
    Retrieve elements from an SQLite export of an Arkindex corpus
    """
    # And load all the elements found in the CTE
    query = (
        list_children(parent_id=parent_id)
        .join(Image)
        .where(Element.type.in_(element_type))
    )

    return query


def build_worker_version_filter(ArkindexModel, worker_versions: List[str | bool]):
    """
    `False` worker version means `manual` worker_version -> null field.
    """
    # Filter `manual` worker version
    condition = ArkindexModel.worker_run.is_null() if False in worker_versions else None

    # Filter other worker versions
    worker_versions = list(filter(None, worker_versions))
    if worker_versions:
        condition |= ArkindexModel.worker_run.in_(
            WorkerRun.select().where(WorkerRun.worker_version.in_(worker_versions))
        )

    return condition


def build_worker_run_filter(ArkindexModel, worker_runs: List[str | bool]):
    """
    `False` worker run means `manual` worker_run -> null field.
    """
    condition = None
    for worker_run in worker_runs:
        condition |= (
            ArkindexModel.worker_run == worker_run
            if worker_run
            else ArkindexModel.worker_run.is_null()
        )
    return condition


def get_transcriptions(
    element_id: str,
    transcription_worker_versions: List[str | bool],
    transcription_worker_runs: List[str | bool],
) -> List[Transcription]:
    """
    Retrieve transcriptions from an SQLite export of an Arkindex corpus
    """
    query = (
        Transcription.select(
            Transcription.id,
            Transcription.text,
            WorkerRun.id.alias("worker_run"),
            WorkerRun.worker_version,
        )
        .join(WorkerRun, JOIN.LEFT_OUTER, on=Transcription.worker_run)
        .where((Transcription.element == element_id))
    )

    if transcription_worker_versions:
        query = query.where(
            build_worker_version_filter(
                Transcription, worker_versions=transcription_worker_versions
            )
        )

    if transcription_worker_runs:
        query = query.where(
            build_worker_run_filter(
                Transcription, worker_runs=transcription_worker_runs
            )
        )

    return query


def get_transcription_entities(
    transcription_id: str,
    entity_worker_versions: List[str | bool],
    entity_worker_runs: List[str | bool],
    supported_types: List[str],
) -> List[TranscriptionEntity]:
    """
    Retrieve transcription entities from an SQLite export of an Arkindex corpus
    """
    query = (
        TranscriptionEntity.select(
            EntityType.name.alias("type"),
            Entity.name.alias("name"),
            TranscriptionEntity.offset,
            TranscriptionEntity.length,
            WorkerRun.id.alias("worker_run"),
            WorkerRun.worker_version,
        )
        .join(Entity, on=TranscriptionEntity.entity)
        .join(EntityType, on=Entity.type)
        .switch(TranscriptionEntity)
        .join(WorkerRun, JOIN.LEFT_OUTER, on=TranscriptionEntity.worker_run)
        .where(
            TranscriptionEntity.transcription == transcription_id,
            EntityType.name.in_(supported_types),
        )
    )

    if entity_worker_versions:
        query = query.where(
            build_worker_version_filter(
                TranscriptionEntity, worker_versions=entity_worker_versions
            )
        )

    if entity_worker_runs:
        query = query.where(
            build_worker_run_filter(TranscriptionEntity, worker_runs=entity_worker_runs)
        )

    return query.order_by(
        TranscriptionEntity.offset, TranscriptionEntity.length.desc()
    ).dicts()
