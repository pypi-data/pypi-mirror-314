# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import json
import re
from operator import methodcaller
from typing import NamedTuple

import pytest

from arkindex_export import (
    Element,
    Transcription,
    TranscriptionEntity,
)
from dan.datasets.extract.arkindex import ArkindexExtractor
from dan.datasets.extract.db import get_transcription_entities
from dan.datasets.extract.exceptions import (
    NoTranscriptionError,
)
from dan.datasets.extract.utils import (
    EntityType,
    entities_to_xml,
    normalize_linebreaks,
    normalize_spaces,
)
from dan.utils import parse_tokens
from tests import FIXTURES, change_split_content

EXTRACTION_DATA_PATH = FIXTURES / "extraction"

ENTITY_TOKEN_SPACE = re.compile(r"[ⓢ|ⓕ|ⓑ] ")
TWO_SPACES_LM_REGEX = re.compile(r"▁ ▁")

# NamedTuple to mock actual database result
Entity = NamedTuple("Entity", offset=int, length=int, type=str, value=str)

TOKENS = {
    "P": EntityType(start="ⓟ", end="Ⓟ"),
    "D": EntityType(start="ⓓ", end="Ⓓ"),
    "N": EntityType(start="ⓝ", end="Ⓝ"),
    "I": EntityType(start="ⓘ", end="Ⓘ"),
}


def filter_tokens(keys):
    return {key: value for key, value in TOKENS.items() if key in keys}


@pytest.mark.parametrize(
    "text,trimmed",
    (
        ("no_spaces", "no_spaces"),
        (" beginning", "beginning"),
        ("ending ", "ending"),
        (" both ", "both"),
        ("    consecutive", "consecutive"),
        ("\ttab", "tab"),
        ("\t tab", "tab"),
        (" \ttab", "tab"),
        ("no|space", "no|space"),
    ),
)
def test_normalize_spaces(text, trimmed):
    assert normalize_spaces(text) == trimmed


@pytest.mark.parametrize(
    "text,trimmed",
    (
        ("no_linebreaks", "no_linebreaks"),
        ("\nbeginning", "beginning"),
        ("ending\n", "ending"),
        ("\nboth\n", "both"),
        ("\n\n\nconsecutive", "consecutive"),
        ("\rcarriage_return", "carriage_return"),
        ("\r\ncarriage_return+linebreak", "carriage_return+linebreak"),
        ("\n\r\r\n\ncarriage_return+linebreak", "carriage_return+linebreak"),
        ("no|linebreaks", "no|linebreaks"),
    ),
)
def test_normalize_linebreaks(text, trimmed):
    assert normalize_linebreaks(text) == trimmed


@pytest.mark.parametrize("load_entities", [True, False])
@pytest.mark.parametrize("keep_spaces", [True, False])
@pytest.mark.parametrize(
    "transcription_entities_worker_version", ["worker_version_id", False]
)
@pytest.mark.parametrize("existing", ((True, False)))
def test_extract(
    load_entities,
    keep_spaces,
    transcription_entities_worker_version,
    split_content,
    mock_database,
    tmp_path,
    existing,
):
    output = tmp_path / "extraction"
    output.mkdir(parents=True, exist_ok=True)

    # Mock tokens
    tokens_path = EXTRACTION_DATA_PATH / "tokens.yml"
    tokens = [
        token
        for entity_type in parse_tokens(tokens_path).values()
        for token in [entity_type.start, entity_type.end]
        if token
    ]

    if existing:
        data = {
            "dataset-id": "dataset-id",
            "image": {
                "iiif_url": f"{FIXTURES}/extraction/images/text_line/test-page_1-line_1.jpg",
                "polygon": [
                    [37, 191],
                    [37, 339],
                    [767, 339],
                    [767, 191],
                    [37, 191],
                ],
            },
            "text": "%",
        }

        (output / "split.json").write_text(
            json.dumps({"train": {"train-page_1-line_5": data}})
        )

        split_content["train"]["train-page_1-line_5"] = data

    extractor = ArkindexExtractor(
        dataset_ids=["dataset_id"],
        element_type=["text_line"],
        output=output,
        # Keep the whole text
        entity_separators=None,
        transcription_worker_versions=[transcription_entities_worker_version],
        entity_worker_versions=[transcription_entities_worker_version]
        if load_entities
        else [],
        tokens=tokens_path if load_entities else None,
        keep_spaces=keep_spaces,
    )

    extractor.run()

    assert sorted(filter(methodcaller("is_file"), output.rglob("*"))) == [
        output / "split.json"
    ]

    split_content, _ = change_split_content(
        load_entities,
        transcription_entities_worker_version,
        keep_spaces,
        split_content,
        tokens,
    )

    assert json.loads((output / "split.json").read_text()) == split_content


@pytest.mark.parametrize("allow_empty", (True, False))
def test_empty_transcription(allow_empty, mock_database, tmp_path):
    output = tmp_path / "extraction"
    extractor = ArkindexExtractor(
        element_type=["text_line"],
        entity_separators=None,
        allow_empty=allow_empty,
        output=output,
    )
    element_no_transcription = Element(id="unknown")
    if allow_empty:
        assert extractor.extract_transcription(element_no_transcription) == ""
    else:
        with pytest.raises(NoTranscriptionError):
            extractor.extract_transcription(element_no_transcription)


@pytest.mark.parametrize("tokens", (None, EXTRACTION_DATA_PATH / "tokens.yml"))
def test_extract_transcription_no_translation(mock_database, tokens, tmp_path):
    output = tmp_path / "extraction"
    extractor = ArkindexExtractor(
        element_type=["text_line"],
        entity_separators=None,
        tokens=tokens,
        output=output,
    )

    element = Element.get_by_id("test-page_1-line_1")
    # Deleting one of the two transcriptions from the element
    Transcription.get(
        Transcription.element == element,
        Transcription.worker_run == "worker_run_id",
    ).delete_instance(recursive=True)

    # Deleting all entities on the element remaining transcription while leaving the transcription intact
    if tokens:
        TranscriptionEntity.delete().where(
            TranscriptionEntity.transcription
            == Transcription.select().where(Transcription.element == element).get()
        ).execute()

    # Early return with only the element transcription text instead of a translation
    assert extractor.extract_transcription(element) == "Leunaut  Claude  49"


@pytest.mark.parametrize(
    "nestation, xml_output, separators",
    (
        # Non-nested
        (
            "non-nested",
            "<root>The <adj>great</adj> king <name>Charles</name> III has eaten \nwith <person>us</person>.</root>",
            None,
        ),
        # Non-nested no text between entities
        (
            "non-nested",
            "<root><adj>great</adj> <name>Charles</name>\n<person>us</person></root>",
            ["\n", " "],
        ),
        # Nested
        (
            "nested",
            "<root>The great king <fullname><name>Charles</name> III</fullname> has eaten \nwith <person>us</person>.</root>",
            None,
        ),
        # Nested no text between entities
        (
            "nested",
            "<root><fullname><name>Charles</name> III</fullname>\n<person>us</person></root>",
            ["\n", " "],
        ),
        # Special characters in entities
        (
            "special-chars",
            "<root>The <Arkindex_s_entity>great</Arkindex_s_entity> king <_Name_1_>Charles</_Name_1_> III has eaten \nwith <Person_>us</Person_>.</root>",
            None,
        ),
    ),
)
def test_entities_to_xml(mock_database, nestation, xml_output, separators):
    transcription = Transcription.get_by_id("tr-with-entities")
    assert (
        entities_to_xml(
            text=transcription.text,
            predictions=get_transcription_entities(
                transcription_id="tr-with-entities",
                entity_worker_versions=[f"worker-version-{nestation}-id"],
                entity_worker_runs=[f"worker-run-{nestation}-id"],
                supported_types=[
                    "name",
                    "fullname",
                    "person",
                    "adj",
                    "Arkindex's entity",
                    '"Name" (1)',
                    "Person /!\\",
                ],
            ),
            entity_separators=separators,
        )
        == xml_output
    )


@pytest.mark.parametrize(
    "supported_entities, xml_output, separators",
    (
        # <adj> missing, no text between entities
        (
            ["name", "person"],
            "<root><name>Charles</name>\n<person>us</person></root>",
            ["\n", " "],
        ),
        # <adj> missing, text between entities
        (
            ["name", "person"],
            "<root>The great king <name>Charles</name> III has eaten \nwith <person>us</person>.</root>",
            None,
        ),
    ),
)
def test_entities_to_xml_partial_entities(
    mock_database, supported_entities, xml_output, separators
):
    transcription = Transcription.get_by_id("tr-with-entities")
    assert (
        entities_to_xml(
            text=transcription.text,
            predictions=get_transcription_entities(
                transcription_id="tr-with-entities",
                entity_worker_versions=["worker-version-non-nested-id"],
                entity_worker_runs=["worker-run-non-nested-id"],
                supported_types=supported_entities,
            ),
            entity_separators=separators,
        )
        == xml_output
    )


@pytest.mark.parametrize(
    "transcription",
    (
        "Something\n",
        "Something\r",
        "Something\t",
        'Something"',
        "Something'",
        "Something<",
        "Something>",
        "Something&",
    ),
)
def test_entities_to_xml_no_encode(transcription):
    assert (
        entities_to_xml(
            text=transcription,
            # Empty queryset
            predictions=TranscriptionEntity.select().where(TranscriptionEntity.id == 0),
            entity_separators=None,
        )
        == f"<root>{transcription}</root>"
    )
