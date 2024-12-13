# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import json
import logging
import pickle
from operator import attrgetter, methodcaller
from pathlib import Path

import pytest
from PIL import Image, ImageChops

from dan.datasets.download.images import (
    IIIF_FULL_SIZE,
    ImageDownloader,
    output_attr_required,
)
from dan.datasets.download.utils import download_image
from dan.utils import parse_tokens
from line_image_extractor.image_utils import BoundingBox
from tests import FIXTURES, change_split_content

EXTRACTION_DATA_PATH = FIXTURES / "extraction"


@pytest.mark.parametrize(
    "max_width, max_height, width, height, resize",
    (
        (1000, 2000, 900, 800, IIIF_FULL_SIZE),
        (1000, 2000, 1100, 800, "1000,"),
        (1000, 2000, 1100, 2800, ",2000"),
        (1000, 2000, 2000, 3000, "1000,"),
    ),
)
def test_get_iiif_size_arg(max_width, max_height, width, height, resize, tmp_path):
    split_path = tmp_path / "output" / "split.json"
    split_path.parent.mkdir()
    split_path.write_text(json.dumps({"train": {}}))

    assert (
        ImageDownloader(
            output=split_path.parent, max_width=max_width, max_height=max_height
        ).get_iiif_size_arg(width=width, height=height)
        == resize
    )


@pytest.mark.parametrize("load_entities", [True, False])
@pytest.mark.parametrize("keep_spaces", [True, False])
@pytest.mark.parametrize(
    "transcription_entities_worker_version", ["worker_version_id", False]
)
def test_download(
    load_entities,
    keep_spaces,
    transcription_entities_worker_version,
    split_content,
    monkeypatch,
    tmp_path,
):
    output = tmp_path / "download"
    output.mkdir(parents=True, exist_ok=True)

    # Mock tokens
    tokens_path = EXTRACTION_DATA_PATH / "tokens.yml"
    tokens = [
        token
        for entity_type in parse_tokens(tokens_path).values()
        for token in [entity_type.start, entity_type.end]
        if token
    ]

    # Mock "split.json"
    split_content, expected_labels = change_split_content(
        load_entities,
        transcription_entities_worker_version,
        keep_spaces,
        split_content,
        tokens,
        {
            "test": {
                "images/test/dataset_id/test-page_1-line_1.jpg": "ⓢLeunaut  ⓕClau⁇e  ⓑ⁇⁇",
                "images/test/dataset_id/test-page_1-line_2.jpg": "ⓢ⁇aurac⁇o  ⓕClau⁇ine  ⓑ⁇⁇",
                "images/test/dataset_id/test-page_1-line_3.jpg": "ⓢLaurent  ⓕJac⁇use  ⓑ21",
                "images/test/dataset_id/test-page_2-line_1.jpg": "ⓢ⁇alette  ⓕElisa⁇et⁇  ⓑ7⁇",
                "images/test/dataset_id/test-page_2-line_2.jpg": "ⓢTan⁇ol  ⓕJean  ⓑ7⁇",
                "images/test/dataset_id/test-page_2-line_3.jpg": "ⓢ⁇auret  ⓕJean  ⓑ⁇⁇",
            },
            "train": {
                "images/train/dataset_id/train-page_1-line_1.jpg": "ⓢLaulont  ⓕFrancois  ⓑ8",
                "images/train/dataset_id/train-page_1-line_2.jpg": "ⓢCiret  ⓕAntoine  ⓑ27",
                "images/train/dataset_id/train-page_1-line_3.jpg": "ⓢCiret  ⓕMarie  ⓑ28",
                "images/train/dataset_id/train-page_1-line_4.jpg": "ⓢCiret  ⓕMarie  ⓑ2",
                "images/train/dataset_id/train-page_2-line_1.jpg": "ⓢEureston  ⓕSolange  ⓑ10",
                "images/train/dataset_id/train-page_2-line_2.jpg": "ⓢTerontussieux  ⓕJean  ⓑ2",
                "images/train/dataset_id/train-page_2-line_3.jpg": "ⓢPressonet  ⓕMarie  ⓑ12",
            },
            "val": {
                "images/val/dataset_id/val-page_1-line_1.jpg": "ⓢCirau⁇  ⓕAntoine  ⓑ⁇⁇",
                "images/val/dataset_id/val-page_1-line_2.jpg": "ⓢCirau⁇  ⓕPriser  ⓑ⁇⁇",
                "images/val/dataset_id/val-page_1-line_3.jpg": "ⓢCirau⁇  ⓕElisa⁇et⁇  ⓑ⁇⁇",
            },
        },
    )
    (output / "split.json").write_text(json.dumps(split_content))

    # Mock download_image so that it simply opens it with Pillow
    monkeypatch.setattr(
        "dan.datasets.download.images.download_image", lambda url: Image.open(url)
    )

    def mock_build_image_url(polygon, image_url, *args, **kwargs):
        # During tests, the image URL is its local path
        return image_url

    extractor = ImageDownloader(
        output=output,
        image_extension=".jpg",
    )
    # Mock build_image_url to simply return the path to the image
    extractor.build_iiif_url = mock_build_image_url
    extractor.run()

    # Check files
    IMAGE_DIR = output / "images"
    TEST_DIR = IMAGE_DIR / "test" / "dataset_id"
    TRAIN_DIR = IMAGE_DIR / "train" / "dataset_id"
    VAL_DIR = IMAGE_DIR / "val" / "dataset_id"

    expected_paths = [
        output / "charset.pkl",
        # Images of test folder
        TEST_DIR / "test-page_1-line_1.jpg",
        TEST_DIR / "test-page_1-line_2.jpg",
        TEST_DIR / "test-page_1-line_3.jpg",
        TEST_DIR / "test-page_2-line_1.jpg",
        TEST_DIR / "test-page_2-line_2.jpg",
        TEST_DIR / "test-page_2-line_3.jpg",
        # Images of train folder
        TRAIN_DIR / "train-page_1-line_1.jpg",
        TRAIN_DIR / "train-page_1-line_2.jpg",
        TRAIN_DIR / "train-page_1-line_3.jpg",
        TRAIN_DIR / "train-page_1-line_4.jpg",
        TRAIN_DIR / "train-page_2-line_1.jpg",
        TRAIN_DIR / "train-page_2-line_2.jpg",
        TRAIN_DIR / "train-page_2-line_3.jpg",
        # Images of val folder
        VAL_DIR / "val-page_1-line_1.jpg",
        VAL_DIR / "val-page_1-line_2.jpg",
        VAL_DIR / "val-page_1-line_3.jpg",
        output / "labels.json",
        output / "split.json",
    ]
    assert sorted(filter(methodcaller("is_file"), output.rglob("*"))) == expected_paths

    # Check "charset.pkl"
    expected_charset = {"⁇"}
    for values in split_content["train"].values():
        expected_charset.update(set(values["text"]))

    if load_entities:
        expected_charset.update(tokens)

    assert set(pickle.loads((output / "charset.pkl").read_bytes())) == expected_charset

    # Check "labels.json"
    assert json.loads((output / "labels.json").read_text()) == expected_labels

    # Check cropped images
    for expected_path in expected_paths:
        if expected_path.suffix != ".jpg":
            continue

        assert ImageChops.difference(
            Image.open(EXTRACTION_DATA_PATH / "images" / expected_path.name),
            Image.open(expected_path),
        )


def test_download_image_error(monkeypatch, caplog, capsys, tmp_path):
    task = {
        "split": "train",
        "polygon": [],
        "image_url": "deadbeef",
        "destination": Path("/dev/null"),
    }
    monkeypatch.setattr(
        "dan.datasets.download.images.polygon_to_bbox",
        lambda polygon: BoundingBox(0, 0, 0, 0),
    )

    split_path = tmp_path / "output" / "split.json"
    split_path.parent.mkdir()
    split_path.write_text(json.dumps({"train": {}}))

    extractor = ImageDownloader(output=split_path.parent, image_extension=".jpg")

    # Add the key in data
    extractor.data[task["split"]][str(task["destination"])] = "deadbeefdata"

    # Build a random task
    extractor.download_images([task])

    # Key should have been removed
    assert str(task["destination"]) not in extractor.data[task["split"]]

    # Check error log
    assert len(caplog.record_tuples) == 1
    _, level, msg = caplog.record_tuples[0]
    assert level == logging.ERROR
    assert msg == "Failed to download 1 image(s)."

    # Check stdout
    captured = capsys.readouterr()
    assert captured.out == "deadbeef: Image URL must be HTTP(S) for element null\n"


def test_download_image_error_try_max(responses, caplog):
    # An image's URL
    url = (
        "https://blabla.com/iiif/2/image_path.jpg/231,699,2789,3659/full/0/default.jpg"
    )
    fixed_url = (
        "https://blabla.com/iiif/2/image_path.jpg/231,699,2789,3659/max/0/default.jpg"
    )

    # Fake responses error
    responses.add(
        responses.GET,
        url,
        status=400,
    )
    # Correct response with max
    responses.add(
        responses.GET,
        fixed_url,
        status=200,
        body=next((FIXTURES / "prediction" / "images").iterdir()).read_bytes(),
    )

    image = download_image(url)

    assert image
    # We try 3 times with the first URL
    # Then the first try with the new URL is successful
    assert len(responses.calls) == 4
    assert list(map(attrgetter("request.url"), responses.calls)) == [url] * 3 + [
        fixed_url
    ]

    # Check error log
    assert len(caplog.record_tuples) == 2

    # We should only have WARNING levels
    assert set(level for _, level, _ in caplog.record_tuples) == {logging.WARNING}


def test_output_attr_required():
    class TestImageDownloader:
        output: Path | None = None

        @output_attr_required
        def image_downloader_method(self, *args, **kwargs):
            return True

    downloader = TestImageDownloader()

    with pytest.raises(
        AssertionError, match="Define an output folder to download images."
    ):
        downloader.image_downloader_method()

    # Set downloader.output
    downloader.output = Path()
    assert downloader.image_downloader_method()
