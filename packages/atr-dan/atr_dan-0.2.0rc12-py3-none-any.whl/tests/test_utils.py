# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

import pytest
import yaml

from dan.utils import (
    EntityType,
    parse_charset_pattern,
    parse_tokens,
    parse_tokens_pattern,
)


@pytest.mark.parametrize(
    ("tokens", "error_msg"),
    [
        # All should have no end tokens
        (
            {
                "name": {
                    "start": "A",
                    "end": "",
                },
                "surname": {"start": "B", "end": "C"},
            },
            "Some entities have end tokens",
        ),
        # All should have end tokens
        (
            {
                "name": {
                    "start": "A",
                    "end": "C",
                },
                "surname": {"start": "B", "end": ""},
            },
            "Some entities have no end token",
        ),
    ],
)
def test_parse_tokens_errors(tmp_path, tokens, error_msg):
    tokens_path = tmp_path / "tokens.yml"
    tokens_path.write_text(yaml.dump(tokens))

    with pytest.raises(AssertionError, match=error_msg):
        parse_tokens(tokens_path)


@pytest.mark.parametrize(
    ("pattern", "entity_types"),
    [
        # No end tokens
        (
            r"([ⒶⒷⒸ][^ⒶⒷⒸ]*)",
            [EntityType(start="Ⓐ"), EntityType(start="Ⓑ"), EntityType(start="Ⓒ")],
        ),
        # With end tokens
        (
            r"(ⓐ.*?Ⓐ)|(ⓑ.*?Ⓑ)|(ⓒ.*?Ⓒ)",
            [
                EntityType(start="ⓐ", end="Ⓐ"),
                EntityType(start="ⓑ", end="Ⓑ"),
                EntityType(start="ⓒ", end="Ⓒ"),
            ],
        ),
    ],
)
def test_parse_tokens_pattern(pattern: str, entity_types: list[EntityType]):
    assert parse_tokens_pattern(entity_types).pattern == pattern


@pytest.mark.parametrize(
    ("charset", "pattern"),
    [
        (["a", "b", "c"], r"[abc]"),
        (["^", "a", "b", "c"], r"[\^abc]"),
        (
            ["<language>", "[", "<word>", "]", "\\", '"'],
            r'(?:<language>)|(?:<word>)|[\[\]\\"]',
        ),
    ],
)
def test_parse_charset_pattern(charset, pattern):
    assert parse_charset_pattern(charset).pattern == pattern
