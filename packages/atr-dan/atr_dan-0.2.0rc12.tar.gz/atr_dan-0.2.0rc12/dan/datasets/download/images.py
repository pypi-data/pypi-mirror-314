# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import functools
import json
import logging
import pickle
from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor
from itertools import chain
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

from dan.datasets.download.exceptions import ImageDownloadError
from dan.datasets.download.utils import (
    download_image,
    get_bbox,
)
from dan.datasets.extract.arkindex import TRAIN_NAME
from line_image_extractor.extractor import extract
from line_image_extractor.image_utils import (
    BoundingBox,
    Extraction,
    polygon_to_bbox,
)

IMAGES_DIR = "images"  # Subpath to the images directory.

IIIF_URL = "{image_url}/{bbox}/{size}/0/default.jpg"
# IIIF 2.0 uses `full`
IIIF_FULL_SIZE = "full"

logger = logging.getLogger(__name__)


def output_attr_required(func):
    """
    Always check that the output attribute is not null.
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        assert self.output is not None, "Define an output folder to download images."
        return func(self, *args, **kwargs)

    return wrapper


class ImageDownloader:
    """
    Download images from extracted data
    """

    def __init__(
        self,
        output: Path | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
        image_extension: str = "",
        unknown_token: str = "⁇",
    ) -> None:
        self.output: Path | None = output

        self.max_width: int | None = max_width
        self.max_height: int | None = max_height
        self.image_extension: str = image_extension
        self.data: dict[str, dict] = defaultdict(dict)
        self.unknown_token: str = unknown_token

    @output_attr_required
    def load_split_data(self) -> None:
        """
        Load the dataset stored in `split.json` and initializes the charset.
        """
        # Load split file
        split_file = self.output / "split.json"
        self.split: Dict = (
            json.loads(split_file.read_text())
            if split_file and split_file.is_file()
            else {}
        )

        # Create directories
        for split_name in self.split:
            (self.output / IMAGES_DIR / split_name).mkdir(parents=True, exist_ok=True)

        self.charset = set(
            chain.from_iterable(
                split_data["text"] for split_data in self.split[TRAIN_NAME].values()
            )
        )

        # Add unknown token to charset
        self.charset.add(self.unknown_token)

    def check_extraction(self, values: dict) -> str | None:
        # Check dataset_id parameter
        if values.get("dataset_id") is None:
            return "Dataset ID not found"

        # Check image parameters
        if not (image := values.get("image")):
            return "Image information not found"

        # Only support iiif_url with polygon for now
        if not image.get("iiif_url"):
            return "Image IIIF URL not found"
        if not image.get("polygon"):
            return "Image polygon not found"

        # Check text parameter
        if values.get("text") is None:
            return "Text not found"

        if self.unknown_token in values["text"]:
            return "Unknown token found in the transcription text"

    def get_iiif_size_arg(self, width: int, height: int) -> str:
        if (self.max_width is None or width <= self.max_width) and (
            self.max_height is None or height <= self.max_height
        ):
            return IIIF_FULL_SIZE

        bigger_width = self.max_width and width >= self.max_width
        bigger_height = self.max_height and height >= self.max_height

        if bigger_width and bigger_height:
            # Resize to the biggest dim to keep aspect ratio
            # Only resize width is bigger than max size
            # This ratio tells which dim needs the biggest shrinking
            ratio = width * self.max_height / (height * self.max_width)
            return f"{self.max_width}," if ratio > 1 else f",{self.max_height}"
        elif bigger_width:
            return f"{self.max_width},"
        # Only resize height is bigger than max size
        elif bigger_height:
            return f",{self.max_height}"

    def build_iiif_url(
        self, polygon: List[List[int]], image_url: str
    ) -> Tuple[BoundingBox, str]:
        bbox = polygon_to_bbox(polygon)
        size = self.get_iiif_size_arg(width=bbox.width, height=bbox.height)
        # Rotations are done using the lib
        return IIIF_URL.format(image_url=image_url, bbox=get_bbox(polygon), size=size)

    @output_attr_required
    def build_tasks(self) -> List[Dict[str, str]]:
        tasks = []
        for split, items in self.split.items():
            # Create directories
            destination = self.output / IMAGES_DIR / split
            destination.mkdir(parents=True, exist_ok=True)

            for element_id, values in items.items():
                filename = Path(element_id).with_suffix(self.image_extension)

                error = self.check_extraction(values)
                if error:
                    logger.warning(f"{destination / filename}: {error}")
                    continue

                image_path = destination / values["dataset_id"] / filename
                image_path.parent.mkdir(parents=True, exist_ok=True)

                # Replace unknown characters by the unknown token
                if split != TRAIN_NAME:
                    unknown_charset = set(values["text"]) - self.charset
                    values["text"] = values["text"].translate(
                        {
                            ord(unknown_char): self.unknown_token
                            for unknown_char in unknown_charset
                        }
                    )

                # Store a relative path to the label file in case we need to move the data elsewhere
                self.data[split][str(image_path.relative_to(self.output))] = values[
                    "text"
                ]

                # Create task for multithreading pool if image does not exist yet
                if image_path.exists():
                    continue

                polygon = values["image"]["polygon"]
                iiif_url = values["image"]["iiif_url"]
                tasks.append(
                    {
                        "split": split,
                        "polygon": polygon,
                        "image_url": self.build_iiif_url(polygon, iiif_url),
                        "destination": image_path,
                    }
                )
        return tasks

    def get_image(
        self,
        split: str,
        polygon: List[List[int]],
        image_url: str,
        destination: Path,
    ) -> None:
        """Save the element's image to the given path and applies any image operations needed.

        :param split: Dataset split this image belongs to.
        :param polygon: Polygon of the processed element.
        :param image_url: Base IIIF URL of the image.
        :param destination: Where the image should be saved.
        """
        bbox = polygon_to_bbox(polygon)
        try:
            img: Image.Image = download_image(image_url)

            # The polygon's coordinate are in the referential of the full image
            # We need to remove the offset of the bounding rectangle
            polygon = [(x - bbox.x, y - bbox.y) for x, y in polygon]

            # Normalize bbox
            bbox = BoundingBox(x=0, y=0, width=bbox.width, height=bbox.height)

            image = extract(
                img=cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR),
                polygon=np.asarray(polygon).clip(0),
                bbox=bbox,
                extraction_mode=Extraction.boundingRect,
                max_deskew_angle=45,
            )

            cv2.imwrite(str(destination), image)

        except Exception as e:
            raise ImageDownloadError(
                split=split, path=destination, url=image_url, exc=e
            )

    def download_images(self, tasks: List[Dict[str, str]]) -> None:
        """
        Execute each image download task in parallel

        :param tasks: List of tasks to execute.
        """
        failed_downloads = []
        with tqdm(
            desc="Downloading images", total=len(tasks)
        ) as pbar, ThreadPoolExecutor() as executor:

            def process_future(future: Future):
                """
                Callback function called at the end of the thread
                """
                # Update the progress bar count
                pbar.update(1)

                exc = future.exception()
                if exc is None:
                    # No error
                    return
                # If failed, tag for removal
                assert isinstance(exc, ImageDownloadError)
                # Remove transcription from labels dict
                del self.data[exc.split][exc.path]
                # Save tried URL
                failed_downloads.append((exc.url, exc.message))

            # Submit all tasks
            for task in tasks:
                executor.submit(self.get_image, **task).add_done_callback(
                    process_future
                )

        if failed_downloads:
            logger.error(f"Failed to download {len(failed_downloads)} image(s).")
            print(*list(map(": ".join, failed_downloads)), sep="\n")

    @output_attr_required
    def export(self) -> None:
        """
        Writes a `labels.json` file containing a mapping of the images that have been correctly uploaded (identified by its path)
        to the ground-truth transcription (with NER tokens if needed).
        """
        (self.output / "labels.json").write_text(
            json.dumps(
                self.data,
                sort_keys=True,
                indent=4,
            )
        )

        (self.output / "charset.pkl").write_bytes(
            pickle.dumps(sorted(list(self.charset)))
        )

    @output_attr_required
    def run(self) -> None:
        """
        Download the missing images from a `split.json` file and build a `labels.json` file containing
        a mapping of the images that have been correctly uploaded (identified by its path)
        to the ground-truth transcription (with NER tokens if needed).
        """
        self.load_split_data()
        tasks: list[dict[str, str]] = self.build_tasks()
        self.download_images(tasks)
        self.export()


def run(
    output: Path,
    max_width: int | None,
    max_height: int | None,
    image_format: str,
    unknown_token: str,
):
    """
    Download the missing images from a `split.json` file and build a `labels.json` file containing
    a mapping of the images that have been correctly uploaded (identified by its path)
    to the ground-truth transcription (with NER tokens if needed).

    :param output: Path where the `split.json` file is stored and where the data will be generated
    :param max_width: Images larger than this width will be resized to this width
    :param max_height: Images larger than this height will be resized to this height
    :param image_format: Images will be saved under this format
    :param unknown_token: The token used to replace unknown characters.
    """
    ImageDownloader(
        output=output,
        max_width=max_width,
        max_height=max_height,
        image_extension=image_format,
        unknown_token=unknown_token,
    ).run()
