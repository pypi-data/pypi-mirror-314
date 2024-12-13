# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import itertools
import logging
import operator
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

import sentencepiece as spm
from nltk import wordpunct_tokenize

from dan.utils import EntityType, LMTokenMapping

logger = logging.getLogger(__name__)


def get_vocabulary(tokenized_text: List[str]) -> set[str]:
    """
    Compute set of vocabulary from tokenzied text.
    :param tokenized_text: List of tokenized text.
    """
    return sorted(set([token for doc in tokenized_text for token in doc.split()]))


@dataclass
class Tokenizer:
    """
    A multi-level tokenizer (char, subword, word), where the subword tokenizer is trained using sentencepiece.
    :param training_corpus: List of training text.
    :param outdir: Path to save the subword tokenizer.
    :param mapping: Mapping between displayed and encoded versions of special characters.
    :param tokens: Start and end tokens used to represent named entities.
    :param subword_vocab_size: Size of the vocabulary size to use to train the subword tokenizer.
    """

    training_corpus: List[str]
    charset: List[str]
    unknown_token: str
    outdir: Path
    mapping: LMTokenMapping
    tokens: EntityType | None = None
    subword_vocab_size: int = 1000
    sentencepiece_model: spm.SentencePieceProcessor = field(init=False)

    @property
    def prefix(self) -> Path:
        return self.outdir / "subword_tokenizer"

    @property
    def ner_tokens(self) -> List[str]:
        if self.tokens is None:
            return []
        return list(
            itertools.chain(
                map(operator.attrgetter("start"), self.tokens.values()),
                filter(
                    operator.truth,
                    map(operator.attrgetter("end"), self.tokens.values()),
                ),
            )
        )

    @property
    def mapping_tokens(self) -> List[str]:
        return [token.encoded for token in self.mapping]

    @property
    def special_tokens(self) -> List[str]:
        return list(set(itertools.chain(self.mapping_tokens, self.ner_tokens)))

    def __post_init__(self) -> None:
        """
        Train a sentencepiece model on the training corpus.
        """
        # Write the corpus in a text file
        logger.info("Training a sentencepiece model for subword tokenization")
        with NamedTemporaryFile(dir=self.outdir, suffix=".txt", mode="w") as tmp_file:
            tmp_file.write("\n".join(self.training_corpus))
            tmp_file.flush()

            try:
                spm.SentencePieceTrainer.train(
                    input=tmp_file.name,
                    vocab_size=self.subword_vocab_size,
                    model_prefix=self.prefix,
                    user_defined_symbols=self.special_tokens,
                    minloglevel=1,
                )
            except Exception as e:
                logger.warning(
                    f"Failed to train a sentencepiece model for subword tokenization: {e} "
                    "Try again by editing the `--subword-vocab-size` parameter."
                )
                self.sentencepiece_model = None
                return

        # Load the model
        self.sentencepiece_model = spm.SentencePieceProcessor(
            model_file=str(self.prefix.with_suffix(".model"))
        )

    def subword_tokenize(self, text: str) -> str:
        """
        Tokenize into subwords. Sampling is disabled to ensure reproducibility.
        """
        tokens = self.sentencepiece_model.encode(text, out_type=str)
        return " ".join(map("".join, map(self.encode, tokens)))

    def word_tokenize(self, text: str) -> str:
        """
        Tokenize text into a string of space-separated words. Spaces (⎵) and NER tokens are considered as words.
        :param text: Text to be tokenized.
        """
        words = list(map("".join, map(self.encode, wordpunct_tokenize(text))))
        return " ".join(
            [
                f"{word} {self.mapping.space.encoded}"
                if (i != len(words) - 1 and word not in self.ner_tokens)
                else word
                for i, word in enumerate(words)
            ]
        )

    def char_tokenize(self, text: str) -> str:
        """
        Tokenize text into a string of space-separated characters.
        :param text: Text to be tokenized.
        """
        return " ".join(
            [
                char if char in self.charset else self.unknown_token
                for char in self.encode(text)
            ]
        )

    def encode(self, text: List[str]) -> List[str]:
        """
        Encode special tokens.
        :param text: Text to be encoded.
        """
        return map(self.mapping.encode_token, text)
