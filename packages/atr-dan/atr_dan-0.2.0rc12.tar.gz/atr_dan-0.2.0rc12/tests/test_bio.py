# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

import logging

import pytest

from dan.bio import convert
from dan.utils import EntityType

ST_TEXT = """ⒶBryan B ⒷParis ⒸJanuary 1st, 1987
ⒶJoe J ⒷGrenoble ⒸAugust 24, 1995
ⒶHannah H ⒷLille ⒸSeptember 15, 2002"""

ST_ET_TEXT = """ⒶBryanⒷ and ⒶJoeⒷ will visit the ⒸEiffel TowerⒹ in ⒸParisⒹ next ⒺTuesdayⒻ.
ⒶHannahⒷ will visit the ⒸPlace ⒶCharles de GaulleⒷ étoileⒹ on ⒺWednesdayⒻ."""


def test_convert_with_error():
    ner_tokens = {
        "Person": EntityType(start="Ⓐ", end="Ⓑ"),
        "Location": EntityType(start="Ⓒ", end="Ⓓ"),
    }

    with pytest.raises(
        AssertionError, match="Ending token Ⓓ doesn't match the starting token Ⓐ"
    ):
        convert("ⒶFredⒹ", ner_tokens)


def test_convert_with_warnings(caplog):
    ner_tokens = {
        "Person": EntityType(start="Ⓐ", end="Ⓑ"),
        "Location": EntityType(start="Ⓒ", end="Ⓓ"),
    }

    assert convert("BryanⒷ and ⒶJoeⒷ will visit the Eiffel TowerⒹ", ner_tokens).split(
        "\n"
    ) == [
        "Bryan O",
        "and O",
        "Joe B-Person",
        "will O",
        "visit O",
        "the O",
        "Eiffel O",
        "Tower O",
    ]
    assert [(level, message) for _, level, message in caplog.record_tuples] == [
        (
            logging.WARNING,
            "Missing starting token for ending token Ⓑ, skipping the entity",
        ),
        (
            logging.WARNING,
            "Missing starting token for ending token Ⓓ, skipping the entity",
        ),
    ]


def test_convert_starting_tokens():
    ner_tokens = {
        "Person": EntityType(start="Ⓐ"),
        "Location": EntityType(start="Ⓑ"),
        "Date": EntityType(start="Ⓒ"),
    }

    assert convert(ST_TEXT, ner_tokens).split("\n") == [
        "Bryan B-Person",
        "B I-Person",
        "Paris B-Location",
        "January B-Date",
        "1st, I-Date",
        "1987 I-Date",
        "Joe B-Person",
        "J I-Person",
        "Grenoble B-Location",
        "August B-Date",
        "24, I-Date",
        "1995 I-Date",
        "Hannah B-Person",
        "H I-Person",
        "Lille B-Location",
        "September B-Date",
        "15, I-Date",
        "2002 I-Date",
    ]


def test_convert_starting_and_ending_tokens():
    ner_tokens = {
        "Person": EntityType(start="Ⓐ", end="Ⓑ"),
        "Location": EntityType(start="Ⓒ", end="Ⓓ"),
        "Date": EntityType(start="Ⓔ", end="Ⓕ"),
    }

    assert convert(ST_ET_TEXT, ner_tokens).split("\n") == [
        "Bryan B-Person",
        "and O",
        "Joe B-Person",
        "will O",
        "visit O",
        "the O",
        "Eiffel B-Location",
        "Tower I-Location",
        "in O",
        "Paris B-Location",
        "next O",
        "Tuesday B-Date",
        ". O",
        "Hannah B-Person",
        "will O",
        "visit O",
        "the O",
        "Place B-Location",
        "Charles B-Person",
        "de I-Person",
        "Gaulle I-Person",
        "étoile I-Location",
        "on O",
        "Wednesday B-Date",
        ". O",
    ]
