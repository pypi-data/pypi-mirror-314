# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import json
import pickle
import re
from operator import methodcaller

import pytest

from dan.datasets.language_model.build import LanguageModelBuilder
from dan.utils import parse_tokens
from tests import FIXTURES, change_split_content

EXTRACTION_DATA_PATH = FIXTURES / "extraction"

ENTITY_TOKEN_SPACE = re.compile(r"[ⓢ|ⓕ|ⓑ] ")
TWO_SPACES_LM_REGEX = re.compile(r"▁ ▁")


@pytest.mark.parametrize(
    "load_entities,transcription_entities_worker_version,expected_subword_language_corpus",
    (
        (
            True,
            "worker_version_id",
            """▁ ⓢ l a u l ont ▁ ⓕ f r an c oi s ▁ ⓑ 8
▁ ⓢ c i re t ▁ ⓕ an t oi ne ▁ ⓑ 2 7
▁ ⓢ c i re t ▁ ⓕ m a r ie ▁ ⓑ 2 8
▁ ⓢ c i re t ▁ ⓕ m a r ie ▁ ⓑ 2
▁ ⓢ e u re s t on ▁ ⓕ so l an g e ▁ ⓑ 1 0
▁ ⓢ t e r ont u s s ie u x ▁ ⓕ j e an ▁ ⓑ 2
▁ ⓢ p re s s on e t ▁ ⓕ m a r ie ▁ ⓑ 1 2""",
        ),
        (
            False,
            "worker_version_id",
            """▁ la u l ont ▁ f r an c oi s ▁ 8
▁ c i re t ▁ an t oi ne ▁ 2 7
▁ c i re t ▁ m a r ie ▁ 2 8
▁ c i re t ▁ m a r ie ▁ 2
▁ e u res t on ▁ so l an g e ▁ 1 0
▁ t e r ont u ss ie u x ▁ j e an ▁ 2
▁ p res so ne t ▁ m a r ie ▁ 1 2""",
        ),
        (
            True,
            False,
            """▁ ⓢ L a u l o n t ▁ ⓕ F r a n c o i s ▁ ⓑ 8
▁ ⓢ C i r e t ▁ ⓕ A n t o i n e ▁ ⓑ 2 7
▁ ⓢ C i r e t ▁ ⓕ M a r ie ▁ ⓑ 2 8
▁ ⓢ C i r e t ▁ ⓕ M a r ie ▁ ⓑ 2
▁ ⓢ E u r e s t o n ▁ ⓕ S o l a n g e ▁ ⓑ 1 0
▁ ⓢ T e r o n t u s s ie u x ▁ ⓕ J e a n ▁ ⓑ 2
▁ ⓢ P r e s s o n e t ▁ ⓕ M a r ie ▁ ⓑ 1 2""",
        ),
        (
            False,
            False,
            """▁ L a u l ont ▁ F r an c oi s ▁ 8
▁ C i re t ▁ A n t oi n e ▁ 2 7
▁ C i re t ▁ M a r ie ▁ 2 8
▁ C i re t ▁ M a r ie ▁ 2
▁ E u re s t on ▁ S o l an g e ▁ 1 0
▁ T e r ont u s s ie u x ▁ J e an ▁ 2
▁ P re s s on e t ▁ M a r ie ▁ 1 2""",
        ),
    ),
)
@pytest.mark.parametrize("keep_spaces", [True, False])
def test_language_model(
    load_entities,
    keep_spaces,
    transcription_entities_worker_version,
    expected_subword_language_corpus,
    split_content,
    tmp_path,
):
    output = tmp_path / "build"
    (output / "language_model").mkdir(parents=True, exist_ok=True)

    # Mock tokens
    tokens_path = EXTRACTION_DATA_PATH / "tokens.yml"
    tokens = [
        token
        for entity_type in parse_tokens(tokens_path).values()
        for token in [entity_type.start, entity_type.end]
        if token
    ]

    # Mock "labels.json"
    _, labels_content = change_split_content(
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
    (output / "labels.json").write_text(json.dumps(labels_content))

    # Mock "charset.pkl"
    expected_charset = {"⁇"}
    for value in labels_content["train"].values():
        expected_charset.update(set(value))
    if load_entities:
        expected_charset.update(tokens)
    (output / "charset.pkl").write_bytes(pickle.dumps(sorted(list(expected_charset))))

    extractor = LanguageModelBuilder(
        output=output,
        tokens=tokens_path if load_entities else None,
        subword_vocab_size=40,
    )
    extractor.run()

    # Check files
    expected_paths = [
        # Previous files
        output / "charset.pkl",
        output / "labels.json",
        # Language resources
        output / "language_model" / "corpus_characters.txt",
        output / "language_model" / "corpus_subwords.txt",
        output / "language_model" / "corpus_words.txt",
        output / "language_model" / "lexicon_characters.txt",
        output / "language_model" / "lexicon_subwords.txt",
        output / "language_model" / "lexicon_words.txt",
        output / "language_model" / "subword_tokenizer.model",
        output / "language_model" / "subword_tokenizer.vocab",
        output / "language_model" / "tokens.txt",
    ]
    assert sorted(filter(methodcaller("is_file"), output.rglob("*"))) == expected_paths

    # Check "language_corpus.txt"
    expected_char_language_corpus = """ⓢ L a u l o n t ▁ ▁ ⓕ F r a n c o i s ▁ ▁ ⓑ 8
ⓢ C i r e t ▁ ▁ ⓕ A n t o i n e ▁ ▁ ⓑ 2 7
ⓢ C i r e t ▁ ▁ ⓕ M a r i e ▁ ▁ ⓑ 2 8
ⓢ C i r e t ▁ ▁ ⓕ M a r i e ▁ ▁ ⓑ 2
ⓢ E u r e s t o n ▁ ▁ ⓕ S o l a n g e ▁ ▁ ⓑ 1 0
ⓢ T e r o n t u s s i e u x ▁ ▁ ⓕ J e a n ▁ ▁ ⓑ 2
ⓢ P r e s s o n e t ▁ ▁ ⓕ M a r i e ▁ ▁ ⓑ 1 2"""

    expected_word_language_corpus = """ⓢ Laulont ▁ ⓕ Francois ▁ ⓑ 8
ⓢ Ciret ▁ ⓕ Antoine ▁ ⓑ 27
ⓢ Ciret ▁ ⓕ Marie ▁ ⓑ 28
ⓢ Ciret ▁ ⓕ Marie ▁ ⓑ 2
ⓢ Eureston ▁ ⓕ Solange ▁ ⓑ 10
ⓢ Terontussieux ▁ ⓕ Jean ▁ ⓑ 2
ⓢ Pressonet ▁ ⓕ Marie ▁ ⓑ 12"""

    # Transcriptions with worker version are in lowercase
    if transcription_entities_worker_version:
        expected_char_language_corpus = expected_char_language_corpus.lower()
        expected_word_language_corpus = expected_word_language_corpus.lower()
        expected_subword_language_corpus = expected_subword_language_corpus.lower()

    # If we do not load entities, remove tokens
    if not load_entities:
        expected_char_language_corpus = ENTITY_TOKEN_SPACE.sub(
            "", expected_char_language_corpus
        )
        expected_word_language_corpus = ENTITY_TOKEN_SPACE.sub(
            "", expected_word_language_corpus
        )
        expected_subword_language_corpus = ENTITY_TOKEN_SPACE.sub(
            "", expected_subword_language_corpus
        )
    # Replace double spaces with regular space
    if not keep_spaces:
        expected_char_language_corpus = TWO_SPACES_LM_REGEX.sub(
            "▁", expected_char_language_corpus
        )
        expected_word_language_corpus = TWO_SPACES_LM_REGEX.sub(
            "▁", expected_word_language_corpus
        )
        expected_subword_language_corpus = TWO_SPACES_LM_REGEX.sub(
            "▁", expected_subword_language_corpus
        )

    assert (
        output / "language_model" / "corpus_characters.txt"
    ).read_text() == expected_char_language_corpus

    assert (
        output / "language_model" / "corpus_words.txt"
    ).read_text() == expected_word_language_corpus

    assert (
        output / "language_model" / "corpus_subwords.txt"
    ).read_text() == expected_subword_language_corpus

    # Check "language_tokens.txt"
    expected_language_tokens = [
        "▁" if t.isspace() else t for t in sorted(list(expected_charset))
    ]
    expected_language_tokens.append("◌")
    assert (output / "language_model" / "tokens.txt").read_text() == "\n".join(
        expected_language_tokens
    )

    # Check "language_lexicon.txt"
    expected_language_char_lexicon = [f"{t} {t}" for t in expected_language_tokens]
    assert (
        output / "language_model" / "lexicon_characters.txt"
    ).read_text() == "\n".join(expected_language_char_lexicon)

    word_vocab = set([word for word in expected_word_language_corpus.split()])
    expected_language_word_lexicon = [
        f"{word} {' '.join(word)}" for word in sorted(word_vocab)
    ]
    assert (output / "language_model" / "lexicon_words.txt").read_text() == "\n".join(
        expected_language_word_lexicon
    )

    subword_vocab = set(
        [subword for subword in expected_subword_language_corpus.split()]
    )
    expected_language_subword_lexicon = [
        f"{subword} {' '.join(subword)}" for subword in sorted(subword_vocab)
    ]
    assert (
        output / "language_model" / "lexicon_subwords.txt"
    ).read_text() == "\n".join(expected_language_subword_lexicon)


@pytest.mark.parametrize(
    "expected_subword_language_corpus,subword_vocab_size",
    (
        (
            """▁ ⓢ L a u l o n t ▁ ⓕ F r a n c o i s ▁ ⓑ 8
▁ ⓢ C i r e t ▁ ⓕ A n t o i n e ▁ ⓑ 2 7
▁ ⓢ C i r e t ▁ ⓕ M a r ie ▁ ⓑ 2 8
▁ ⓢ C i r e t ▁ ⓕ M a r ie ▁ ⓑ 2
▁ ⓢ E u r e s t o n ▁ ⓕ S o l a n g e ▁ ⓑ 1 0
▁ ⓢ T e r o n t u s s ie u x ▁ ⓕ J e a n ▁ ⓑ 2
▁ ⓢ P r e s s o n e t ▁ ⓕ M a r ie ▁ ⓑ 1 2""",
            40,
        ),
        (
            """▁ ⓢ L a u l ont ▁ ⓕ F r an c oi s ▁ ⓑ 8
▁ ⓢ C i re t ▁ ⓕ A n t oi n e ▁ ⓑ 2 7
▁ ⓢ C i re t ▁ ⓕ M a r ie ▁ ⓑ 2 8
▁ ⓢ C i re t ▁ ⓕ M a r ie ▁ ⓑ 2
▁ ⓢ E u re s t on ▁ ⓕ S o l an g e ▁ ⓑ 1 0
▁ ⓢ T e r ont u s s ie u x ▁ ⓕ J e an ▁ ⓑ 2
▁ ⓢ P re s s on e t ▁ ⓕ M a r ie ▁ ⓑ 1 2""",
            45,
        ),
    ),
)
@pytest.mark.parametrize("keep_spaces", [True, False])
def test_language_model_subword_vocab_size(
    keep_spaces,
    expected_subword_language_corpus,
    subword_vocab_size,
    split_content,
    tmp_path,
):
    output = tmp_path / "build"
    (output / "language_model").mkdir(parents=True, exist_ok=True)

    # Mock tokens
    tokens_path = EXTRACTION_DATA_PATH / "tokens.yml"
    tokens = [
        token
        for entity_type in parse_tokens(tokens_path).values()
        for token in [entity_type.start, entity_type.end]
        if token
    ]

    # Mock "labels.json"
    _, labels_content = change_split_content(
        True,
        False,
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
    (output / "labels.json").write_text(json.dumps(labels_content))

    # Mock "charset.pkl"
    expected_charset = {"⁇"}
    for value in labels_content["train"].values():
        expected_charset.update(set(value))
    expected_charset.update(tokens)
    (output / "charset.pkl").write_bytes(pickle.dumps(sorted(list(expected_charset))))

    extractor = LanguageModelBuilder(
        output=output,
        tokens=tokens_path,
        subword_vocab_size=subword_vocab_size,
    )
    extractor.run()

    # Check files
    expected_paths = [
        # Previous files
        output / "charset.pkl",
        output / "labels.json",
        # Language resources
        output / "language_model" / "corpus_characters.txt",
        output / "language_model" / "corpus_subwords.txt",
        output / "language_model" / "corpus_words.txt",
        output / "language_model" / "lexicon_characters.txt",
        output / "language_model" / "lexicon_subwords.txt",
        output / "language_model" / "lexicon_words.txt",
        output / "language_model" / "subword_tokenizer.model",
        output / "language_model" / "subword_tokenizer.vocab",
        output / "language_model" / "tokens.txt",
    ]
    assert sorted(filter(methodcaller("is_file"), output.rglob("*"))) == expected_paths

    # Check "language_corpus.txt"
    expected_char_language_corpus = """ⓢ L a u l o n t ▁ ▁ ⓕ F r a n c o i s ▁ ▁ ⓑ 8
ⓢ C i r e t ▁ ▁ ⓕ A n t o i n e ▁ ▁ ⓑ 2 7
ⓢ C i r e t ▁ ▁ ⓕ M a r i e ▁ ▁ ⓑ 2 8
ⓢ C i r e t ▁ ▁ ⓕ M a r i e ▁ ▁ ⓑ 2
ⓢ E u r e s t o n ▁ ▁ ⓕ S o l a n g e ▁ ▁ ⓑ 1 0
ⓢ T e r o n t u s s i e u x ▁ ▁ ⓕ J e a n ▁ ▁ ⓑ 2
ⓢ P r e s s o n e t ▁ ▁ ⓕ M a r i e ▁ ▁ ⓑ 1 2"""

    expected_word_language_corpus = """ⓢ Laulont ▁ ⓕ Francois ▁ ⓑ 8
ⓢ Ciret ▁ ⓕ Antoine ▁ ⓑ 27
ⓢ Ciret ▁ ⓕ Marie ▁ ⓑ 28
ⓢ Ciret ▁ ⓕ Marie ▁ ⓑ 2
ⓢ Eureston ▁ ⓕ Solange ▁ ⓑ 10
ⓢ Terontussieux ▁ ⓕ Jean ▁ ⓑ 2
ⓢ Pressonet ▁ ⓕ Marie ▁ ⓑ 12"""

    # Replace double spaces with regular space
    if not keep_spaces:
        expected_char_language_corpus = TWO_SPACES_LM_REGEX.sub(
            "▁", expected_char_language_corpus
        )
        expected_word_language_corpus = TWO_SPACES_LM_REGEX.sub(
            "▁", expected_word_language_corpus
        )
        expected_subword_language_corpus = TWO_SPACES_LM_REGEX.sub(
            "▁", expected_subword_language_corpus
        )

    assert (
        output / "language_model" / "corpus_characters.txt"
    ).read_text() == expected_char_language_corpus

    assert (
        output / "language_model" / "corpus_words.txt"
    ).read_text() == expected_word_language_corpus

    assert (
        output / "language_model" / "corpus_subwords.txt"
    ).read_text() == expected_subword_language_corpus

    # Check "language_tokens.txt"
    expected_language_tokens = [
        "▁" if t.isspace() else t for t in sorted(list(expected_charset))
    ]
    expected_language_tokens.append("◌")
    assert (output / "language_model" / "tokens.txt").read_text() == "\n".join(
        expected_language_tokens
    )

    # Check "language_lexicon.txt"
    expected_language_char_lexicon = [f"{t} {t}" for t in expected_language_tokens]
    assert (
        output / "language_model" / "lexicon_characters.txt"
    ).read_text() == "\n".join(expected_language_char_lexicon)

    word_vocab = set([word for word in expected_word_language_corpus.split()])
    expected_language_word_lexicon = [
        f"{word} {' '.join(word)}" for word in sorted(word_vocab)
    ]
    assert (output / "language_model" / "lexicon_words.txt").read_text() == "\n".join(
        expected_language_word_lexicon
    )

    subword_vocab = set(
        [subword for subword in expected_subword_language_corpus.split()]
    )
    expected_language_subword_lexicon = [
        f"{subword} {' '.join(subword)}" for subword in sorted(subword_vocab)
    ]
    assert (
        output / "language_model" / "lexicon_subwords.txt"
    ).read_text() == "\n".join(expected_language_subword_lexicon)
