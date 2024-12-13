# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-


class ProcessingError(Exception):
    ...


class ElementProcessingError(ProcessingError):
    """
    Raised when a problem is encountered while processing an element
    """

    element_id: str
    """
    ID of the element being processed.
    """

    def __init__(self, element_id: str, *args: object) -> None:
        super().__init__(*args)
        self.element_id = element_id


class NoTranscriptionError(ElementProcessingError):
    """
    Raised when there are no transcriptions on an element
    """

    def __str__(self) -> str:
        return f"No transcriptions found on element ({self.element_id}) with this config. Skipping."
