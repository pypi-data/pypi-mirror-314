# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import pytest
from mdutils.mdutils import MdUtils

from dan.datasets.analyze import read_yaml
from dan.datasets.analyze.statistics import Statistics
from tests.conftest import FIXTURES


@pytest.fixture
def image_statistics():
    return MdUtils(file_name="").read_md_file(str(FIXTURES / "analyze" / "images"))


@pytest.fixture
def labels_statistics():
    return MdUtils(file_name="").read_md_file(str(FIXTURES / "analyze" / "labels"))


@pytest.fixture
def ner_statistics():
    return MdUtils(file_name="").read_md_file(str(FIXTURES / "analyze" / "ner"))


@pytest.fixture
def full_statistics():
    return MdUtils(file_name="").read_md_file(str(FIXTURES / "analyze" / "stats"))


def test_display_image_statistics(image_statistics, tmp_path):
    stats = Statistics(filename=tmp_path)
    stats.create_image_statistics(
        images=[
            "tests/data/training/training_dataset/images/0a34e13a-4ab0-4a91-8d7c-b1d8fee32628.png",
            "tests/data/training/training_dataset/images/0a70e14f-feda-4607-989c-36cf581ddff5.png",
            "tests/data/training/training_dataset/images/0a576062-303c-4893-a729-c09c92865d31.png",
            "tests/data/training/training_dataset/images/0b2457c8-81f1-4600-84d9-f8bf2822a991.png",
            "tests/data/training/training_dataset/images/fb3edb59-3678-49f8-8e16-8e32e3b0f051.png",
            "tests/data/training/training_dataset/images/fe498de2-ece4-4fbe-8b53-edfce1b820f0.png",
        ]
    )
    assert stats.document.get_md_text() == image_statistics


def test_display_label_statistics(labels_statistics, tmp_path):
    filename = tmp_path / "labels.md"
    stats = Statistics(filename=str(filename))
    stats.create_label_statistics(
        labels=[
            "Teklia’s expertise is to develop document analysis\nand processing solutions using, among other things,\nOCR technology.",
            "Our software combines image analysis, printed and\nhandwritten text recognition, text segmentation with\na document classification and indexation system.",
            "Our objective is to deliver to our clients an automated\ndocument processing tool easy-to-use and adapted\nto their needs.",
            "With the same state of mind, we developed additional solutions to\nenhance both security and business-process.",
        ]
    )
    assert stats.document.get_md_text() == labels_statistics


def test_display_ner_statistics(ner_statistics, tmp_path):
    tokens = read_yaml(FIXTURES / "training" / "training_dataset" / "tokens.yaml")
    stats = Statistics(filename=tmp_path)
    stats.create_ner_statistics(
        labels=[
            "ⓈDayon ⒻFernand Ⓐ6\nⓈDayen ⒻMaurice Ⓐ2\nⓈTottelier ⒻJean Baptiste Ⓐ59",
            "ⓈPeryro ⒻEtienne Ⓐ33\nⓈJeannot ⒻCaroline Ⓐ24\nⓈMouline ⒻPierre Ⓐ32",
        ],
        ner_tokens=tokens,
    )
    assert stats.document.get_md_text() == ner_statistics


def test_run(full_statistics, tmp_path):
    output_file = tmp_path / "stats.md"
    stats = Statistics(filename=str(output_file))
    stats.run(
        labels_path=FIXTURES / "training" / "training_dataset" / "labels.json",
        tokens=read_yaml(FIXTURES / "training" / "training_dataset" / "tokens.yaml"),
    )
    assert output_file.read_text() == full_statistics
