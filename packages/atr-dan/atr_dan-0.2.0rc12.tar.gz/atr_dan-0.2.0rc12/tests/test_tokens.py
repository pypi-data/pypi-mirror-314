# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import pytest

from dan.datasets.tokens.generate import LIMIT, OFFSET, get_token, run
from tests import FIXTURES

TOKENS_DATA_PATH = FIXTURES / "tokens"


def test_get_token():
    token_generator = get_token()

    tokens = []
    for _ in range(LIMIT - OFFSET):
        tokens.append(next(token_generator))

    assert tokens == [
        "Ⓐ",
        "Ⓑ",
        "Ⓒ",
        "Ⓓ",
        "Ⓔ",
        "Ⓕ",
        "Ⓖ",
        "Ⓗ",
        "Ⓘ",
        "Ⓙ",
        "Ⓚ",
        "Ⓛ",
        "Ⓜ",
        "Ⓝ",
        "Ⓞ",
        "Ⓟ",
        "Ⓠ",
        "Ⓡ",
        "Ⓢ",
        "Ⓣ",
        "Ⓤ",
        "Ⓥ",
        "Ⓦ",
        "Ⓧ",
        "Ⓨ",
        "Ⓩ",
        "ⓐ",
        "ⓑ",
        "ⓒ",
        "ⓓ",
        "ⓔ",
        "ⓕ",
        "ⓖ",
        "ⓗ",
        "ⓘ",
        "ⓙ",
        "ⓚ",
        "ⓛ",
        "ⓜ",
        "ⓝ",
        "ⓞ",
        "ⓟ",
        "ⓠ",
        "ⓡ",
        "ⓢ",
        "ⓣ",
        "ⓤ",
        "ⓥ",
        "ⓦ",
        "ⓧ",
        "ⓨ",
        "ⓩ",
        "⓪",
        "⓫",
        "⓬",
        "⓭",
        "⓮",
        "⓯",
        "⓰",
        "⓱",
        "⓲",
        "⓳",
        "⓴",
        "⓵",
        "⓶",
        "⓷",
        "⓸",
        "⓹",
        "⓺",
        "⓻",
        "⓼",
        "⓽",
        "⓾",
        "⓿",
    ]


@pytest.mark.parametrize(
    "end_tokens, expected_file",
    [
        (True, TOKENS_DATA_PATH / "end_tokens.yml"),
        (False, TOKENS_DATA_PATH / "no_end_tokens.yml"),
    ],
)
def test_tokens(end_tokens, expected_file, tmp_path):
    output_file = tmp_path / "tokens.yml"

    run(
        entities=FIXTURES / "entities.yml",
        end_tokens=end_tokens,
        output_file=output_file,
    )

    assert output_file.read_text() == expected_file.read_text()
