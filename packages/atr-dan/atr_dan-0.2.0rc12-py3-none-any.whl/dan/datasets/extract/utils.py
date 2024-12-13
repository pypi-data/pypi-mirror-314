# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import logging
import re
from dataclasses import dataclass, field
from typing import Dict, List

from lxml.etree import Element, SubElement, tostring

from arkindex_export import TranscriptionEntity
from dan.utils import EntityType

logger = logging.getLogger(__name__)

# Replace \t with regular space and consecutive spaces
TRIM_SPACE_REGEX = re.compile(r"[\t ]+")
TRIM_RETURN_REGEX = re.compile(r"[\r\n]+")

# Remove invalid characters to build valid XML tag name
SLUG_PATTERN = re.compile(r"[\W]+")

# Some characters are encoded in XML but we don't want them encoded in the end
ENCODING_MAP = {
    "&#13;": "\r",
    "&lt;": "<",
    "&gt;": ">",
    "&amp;": "&",
}


def normalize_linebreaks(text: str) -> str:
    """
    Remove begin/ending linebreaks.
    Replace \r with regular linebreak and consecutive linebreaks.
    :param text: Text to normalize.
    """
    return TRIM_RETURN_REGEX.sub("\n", text.strip())


def normalize_spaces(text: str) -> str:
    """
    Remove begin/ending spaces.
    Replace \t with regular space and consecutive spaces.
    :param text: Text to normalize.
    """
    return TRIM_SPACE_REGEX.sub(" ", text.strip())


def slugify(text: str):
    """
    Replace invalid characters in text to underscores to use it as XML tag.
    """
    return SLUG_PATTERN.sub("_", text)


def get_translation_map(tokens: Dict[str, EntityType]) -> Dict[str, str] | None:
    if not tokens:
        return

    translation_map = {
        # Roots
        "<root>": "",
        "</root>": "",
    }
    # Tokens
    for entity_name, token_type in tokens.items():
        translation_map[f"<{slugify(entity_name)}>"] = token_type.start
        translation_map[f"</{slugify(entity_name)}>"] = token_type.end

    return translation_map


@dataclass
class XMLEntity:
    type: str
    name: str
    offset: int
    length: int
    worker_version: str
    worker_run: str
    children: List["XMLEntity"] = field(default_factory=list)

    @property
    def end(self) -> int:
        return self.offset + self.length

    def add_child(self, child: TranscriptionEntity):
        self.children.append(
            XMLEntity(
                type=child["type"],
                name=child["name"],
                offset=child["offset"] - self.offset,
                length=child["length"],
                worker_version=child["worker_version"],
                worker_run=child["worker_run"],
            )
        )

    def insert(self, parent: Element):
        e = SubElement(parent, slugify(self.type))

        if not self.children:
            # No children
            e.text = self.name
            return

        offset = 0
        for child in self.children:
            # Add text before entity
            portion_before = self.name[offset : child.offset]
            offset += len(portion_before)
            if len(e):
                e[-1].tail = portion_before
            else:
                e.text = portion_before
            child.insert(e)
            offset += child.length

        # Text after the last entity
        e[-1].tail = self.name[self.children[-1].end : self.end]


def entities_to_xml(
    text: str,
    predictions: List[TranscriptionEntity],
    entity_separators: List[str] | None = None,
) -> str:
    """Represent the transcription and its entities in XML format. Each entity will be exposed with an XML tag.
    Its type will be used to name the tag.

    :param text: The text of the transcription
    :param predictions: The list of entities linked to the transcription
    :param entity_separators: When provided, instead of adding the text between entities, add one separator encountered in this text. The order is kept when looking for separators. Defaults to None
    :return: The representation of the transcription in XML format
    """

    def _find_separator(transcription: str) -> str:
        """
        Find the first entity separator in the provided transcription.
        """
        for separator in entity_separators:
            if separator in transcription:
                return separator
        return ""

    def add_portion(entity_offset: int | None = None):
        """
        Add the portion of text between entities either:
        - after the last node, if there is one before
        - on this node

        If we remove the text between entities, we keep one of the separators provided. Order matters.
        """
        portion = text[offset:entity_offset]

        if entity_separators:
            # Remove the text except the first entity_separator encountered
            portion = _find_separator(portion)

        if len(root):
            root[-1].tail = portion
        else:
            root.text = portion

    entities = iter(predictions)

    # This will mark the ending position of the first-level of entities
    last_end = None
    parsed: List[XMLEntity] = []

    for entity in entities:
        # First entity is not inside any other
        # If offset is too high, no nestation
        if not last_end or entity["offset"] >= last_end:
            parsed.append(XMLEntity(**entity))
            last_end = entity["offset"] + entity["length"]
            continue

        # Nested entity
        parsed[-1].add_child(entity)

    # XML export
    offset = 0
    root = Element("root")

    for entity in parsed:
        add_portion(entity.offset)

        entity.insert(root)

        offset = entity.end

    # Add text after last entity
    add_portion()

    # Cleanup separators introduced when text was removed
    if entity_separators:
        characters = "".join(entity_separators)
        root.text = root.text.lstrip(characters)
        # Strip trailing spaces on last child
        root[-1].tail = root[-1].tail.rstrip(characters)

    encoded_transcription = tostring(root, encoding="utf-8").decode()
    for pattern, repl in ENCODING_MAP.items():
        encoded_transcription = encoded_transcription.replace(pattern, repl)
    return encoded_transcription
