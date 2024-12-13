# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import json
import logging
import pickle
from collections import defaultdict
from pathlib import Path
from typing import Dict

from dan.datasets.extract.arkindex import TRAIN_NAME
from dan.datasets.language_model.utils import (
    Tokenizer,
    get_vocabulary,
)
from dan.utils import LMTokenMapping, parse_tokens

LANGUAGE_DIR = "language_model"  # Subpath to the language model directory.

logger = logging.getLogger(__name__)


class LanguageModelBuilder:
    """
    Build a language model from extracted data
    """

    def __init__(
        self,
        output: Path | None = None,
        subword_vocab_size: int = 1000,
        unknown_token: str = "⁇",
        tokens: Path | None = None,
    ) -> None:
        self.output = output

        self.unknown_token = unknown_token
        self.tokens = parse_tokens(tokens) if tokens else {}

        self.subword_vocab_size = subword_vocab_size
        self.mapping = LMTokenMapping()

        self.language_corpus = defaultdict(list)
        self.language_tokens = []
        self.language_lexicon = defaultdict(list)

        # Load labels file
        labels_file = self.output / "labels.json" if self.output else None
        self.labels: Dict = (
            json.loads(labels_file.read_text())
            if labels_file and labels_file.is_file()
            else {}
        )

        # Load charset file
        charset_file = self.output / "charset.pkl" if self.output else None
        self.charset: Dict = (
            pickle.loads(charset_file.read_bytes())
            if charset_file and charset_file.is_file()
            else {}
        )

    def format_lm_files(self) -> None:
        """
        Convert charset to a LM-compatible charset. Ensure that special LM tokens do not appear in the charset.
        """
        logger.info("Preparing language resources")

        # Build LM tokens
        for token in sorted(list(self.charset)):
            assert (
                token not in self.mapping.encode.values()
            ), f"Special token {token} is reserved for language modeling."
            self.language_tokens.append(
                self.mapping.encode[token]
            ) if token in self.mapping.encode else self.language_tokens.append(token)
        self.language_tokens.append(self.mapping.ctc.encoded)

        # Build LM corpus
        train_corpus = [
            value.replace(self.mapping.linebreak.display, self.mapping.space.display)
            for value in self.labels[TRAIN_NAME].values()
        ]

        tokenizer = Tokenizer(
            training_corpus=train_corpus,
            charset=self.language_tokens,
            unknown_token=self.unknown_token,
            outdir=self.output / LANGUAGE_DIR,
            mapping=self.mapping,
            tokens=self.tokens,
            subword_vocab_size=self.subword_vocab_size,
        )

        if not tokenizer.sentencepiece_model:
            return

        for level, tokenize in (
            ("characters", tokenizer.char_tokenize),
            ("words", tokenizer.word_tokenize),
            ("subwords", tokenizer.subword_tokenize),
        ):
            self.language_corpus[level] = list(map(tokenize, train_corpus))

        # Build LM lexicon
        self.language_lexicon["characters"] = [
            f"{token} {token}" for token in self.language_tokens
        ]
        for level in ["words", "subwords"]:
            self.language_lexicon[level] = [
                f"{token} {tokenizer.char_tokenize(token)}"
                for token in get_vocabulary(self.language_corpus[level])
            ]

    def export(self) -> None:
        """
        Writes all files needed for the language model
        """
        for level in ["characters", "words", "subwords"]:
            (self.output / LANGUAGE_DIR / f"corpus_{level}.txt").write_text(
                "\n".join(self.language_corpus[level])
            )
            (self.output / LANGUAGE_DIR / f"lexicon_{level}.txt").write_text(
                "\n".join(self.language_lexicon[level])
            )

        (self.output / LANGUAGE_DIR / "tokens.txt").write_text(
            "\n".join(self.language_tokens)
        )

    def run(self) -> None:
        """
        Build and write all files needed for the language model
        """
        self.format_lm_files()
        self.export()


def run(
    output: Path,
    subword_vocab_size: int,
    unknown_token: str,
    tokens: Path | None,
):
    """
    Build and write all files needed for the language model

    :param output: Path where the `split.json` file is stored and where the data will be generated
    :param subword_vocab_size: The size of the subword vocabulary.
    :param unknown_token: The token used to replace unknown characters.
    :param tokens: Mapping between starting tokens and end tokens to extract text with their entities.
    """
    (output / LANGUAGE_DIR).mkdir(parents=True, exist_ok=True)

    LanguageModelBuilder(
        output=output,
        subword_vocab_size=subword_vocab_size,
        unknown_token=unknown_token,
        tokens=tokens,
    ).run()
