# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
from operator import itemgetter
from pathlib import Path

import yaml

from arkindex_export import EntityType, open_database


def run(database: Path, output_file: Path) -> None:
    # Load SQLite database
    open_database(database)

    # Extract and save entities to YAML
    entities = list(
        map(itemgetter(0), EntityType.select(EntityType.name).distinct().tuples())
    )

    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(
        yaml.safe_dump({"entities": entities}, explicit_start=True, allow_unicode=True)
    )
