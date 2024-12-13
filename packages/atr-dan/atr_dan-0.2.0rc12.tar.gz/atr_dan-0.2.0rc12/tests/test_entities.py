# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
from dan.datasets.entities.extract import run
from tests import FIXTURES


def test_entities(mock_database, tmp_path):
    output_file = tmp_path / "entities.yml"

    run(database=mock_database, output_file=output_file)

    assert output_file.read_text() == (FIXTURES / "entities.yml").read_text()
