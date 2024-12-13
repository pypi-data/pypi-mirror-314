# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import logging
from collections import Counter, defaultdict
from functools import partial
from pathlib import Path
from typing import Dict, List

import imagesize
import numpy as np
from mdutils.mdutils import MdUtils
from prettytable import MARKDOWN, PrettyTable

from dan.ocr import wandb
from dan.utils import read_json

logger = logging.getLogger(__name__)

METRIC_COLUMN = "Metric"


def create_table(
    data: Dict,
    count: bool = False,
    total: bool = True,
):
    """
    Each keys will be made into a column
    We compute min, max, mean, median, total by default.
    Total can be disabled. Count (length) computation can be enabled.
    """

    statistics = PrettyTable(field_names=[METRIC_COLUMN, *data.keys()])
    statistics.align.update({METRIC_COLUMN: "l"})
    statistics.set_style(MARKDOWN)

    operations = []

    if count:
        operations.append(("Count", len, None))

    operations.extend(
        [
            ("Min", np.min, None),
            ("Max", np.max, None),
            ("Mean", np.mean, 2),
            ("Median", np.median, 2),
        ]
    )
    if total:
        operations.append(("Total", np.sum, None))

    statistics.add_rows(
        [
            [
                col_name,
                *list(
                    map(
                        # Round values if needed
                        partial(round, ndigits=digits),
                        map(operator, data.values()),
                    )
                ),
            ]
            for col_name, operator, digits in operations
        ]
    )

    return statistics


class Statistics:
    HEADERS = {
        "Images": "Images statistics",
        "Labels": "Labels statistics",
        "Chars": "Characters statistics",
        "Tokens": "NER tokens statistics",
    }

    def __init__(self, filename: str) -> None:
        self.document = MdUtils(file_name=filename, title="Statistics")

    def _write_section(self, table: PrettyTable, title: str, level: int = 2):
        """
        Write the new section in the file.

        <title with appropriate level>

        <table>

        """
        self.document.new_header(level=level, title=title, add_table_of_contents="n")
        self.document.write("\n")

        logger.info(f"{title}\n\n{table}\n")

        self.document.write(table.get_string())
        self.document.write("\n")

    def create_image_statistics(self, images: List[str]):
        """
        Compute statistics on image sizes and write them to file.
        """
        shapes = list(map(imagesize.get, images))
        widths, heights = zip(*shapes)

        self._write_section(
            table=create_table(
                data={"Width": widths, "Height": heights}, count=True, total=False
            ),
            title=Statistics.HEADERS["Images"],
        )

    def create_label_statistics(self, labels: List[str]):
        """
        Compute statistics on text labels and write them to file.
        """
        char_counter = Counter()
        data = defaultdict(list)

        for text in labels:
            char_counter.update(text)
            data["Chars"].append(len(text))
            data["Words"].append(len(text.split()))
            data["Lines"].append(len(text.split("\n")))

        self._write_section(
            table=create_table(data=data),
            title=Statistics.HEADERS["Labels"],
        )

        self.create_character_occurrences_statistics(char_counter)

    def create_character_occurrences_statistics(self, char_counter: Counter):
        """
        Compute statistics on the character distribution and write them to file.
        """
        char_occurrences = PrettyTable(
            field_names=["Character", "Occurrence"],
        )
        char_occurrences.align.update({"Character": "l", "Occurrence": "r"})
        char_occurrences.set_style(MARKDOWN)
        char_occurrences.add_rows(list(char_counter.most_common()))

        self._write_section(
            table=char_occurrences, title=Statistics.HEADERS["Chars"], level=3
        )

    def create_ner_statistics(self, labels: List[str], ner_tokens: Dict) -> str:
        """
        Compute statistics on ner tokens presence.
        """
        entity_counter = defaultdict(list)
        for text in labels:
            for ner_label, token in ner_tokens.items():
                entity_counter[ner_label].append(text.count(token["start"]))

        self._write_section(
            table=create_table(data=entity_counter),
            title=Statistics.HEADERS["Tokens"],
            level=3,
        )

    def run(self, labels_path: Path, tokens: Dict | None):
        labels = read_json(labels_path)

        # Iterate over each split
        for split_name, split_data in labels.items():
            self.document.new_header(level=1, title=split_name.capitalize())

            # Image statistics
            # Path to the images are the key of the dict
            self.create_image_statistics(
                images=[labels_path.parent / image_path for image_path in split_data]
            )

            labels = list(split_data.values())
            # Text statistics
            self.create_label_statistics(labels=labels)

            if tokens is not None:
                self.create_ner_statistics(labels=labels, ner_tokens=tokens)
        self.document.create_md_file()


def run(
    labels: Path,
    tokens: Dict | None,
    output: Path,
    wandb_params: dict | None,
) -> None:
    """
    Compute and save a dataset statistics.
    """
    Statistics(filename=str(output)).run(labels_path=labels, tokens=tokens)

    # Publish file on "Weights & Biases"
    wandb.init(
        wandb_params,
        config={
            wandb.Config.ANALYZE.value: {
                "wandb": wandb_params,
                "labels": labels,
                "tokens": tokens,
                "output": output,
            }
        },
        output_folder=output.parent,
    )
    artifact = wandb.artifact(
        name=f"run-{wandb.run_id()}-statistics",
        type="markdown",
        description="Statistics metrics",
    )
    wandb.log_artifact(artifact, local_path=output, name=output.name)
