# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
from pathlib import Path


class ImageDownloadError(Exception):
    """
    Raised when an element's image could not be downloaded
    """

    def __init__(
        self, split: str, path: Path, url: str, exc: Exception, *args: object
    ) -> None:
        super().__init__(*args)
        self.split: str = split
        self.path: str = str(path)
        self.url: str = url
        self.message = f"{str(exc)} for element {path.stem}"
