# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import logging
from io import BytesIO
from typing import List

import requests
from PIL import Image, ImageOps
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

# See http://docs.python-requests.org/en/master/user/advanced/#timeouts
DOWNLOAD_TIMEOUT = (30, 60)


def _retry_log(retry_state, *args, **kwargs):
    logger.warning(
        f"Request to {retry_state.args[0]} failed ({repr(retry_state.outcome.exception())}), "
        f"retrying in {retry_state.idle_for} seconds"
    )


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2),
    retry=retry_if_exception_type(requests.RequestException),
    before_sleep=_retry_log,
    reraise=True,
)
def _retried_request(url: str) -> requests.Response:
    resp = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
    resp.raise_for_status()
    return resp


def download_image(url: str) -> Image.Image:
    """
    Download an image and open it with Pillow
    """
    assert url.startswith("http"), "Image URL must be HTTP(S)"

    # Download the image
    # Cannot use stream=True as urllib's responses do not support the seek(int) method,
    # which is explicitly required by Image.open on file-like objects
    try:
        resp = _retried_request(url)
    except requests.HTTPError as e:
        if "/full/" in url and 400 <= e.response.status_code < 500:
            # Retry with max instead of full as IIIF size
            resp = _retried_request(url.replace("/full/", "/max/"))
        else:
            raise e

    # Preprocess the image and prepare it for classification
    image = Image.open(BytesIO(resp.content)).convert("RGB")

    # Do not rotate JPEG images (see https://github.com/python-pillow/Pillow/issues/4703)
    image = ImageOps.exif_transpose(image)

    logger.debug(
        "Downloaded image {} - size={}x{}".format(url, image.size[0], image.size[1])
    )

    return image


def get_bbox(polygon: List[List[int]]) -> str:
    """
    Returns a comma-separated string of upper left-most pixel, width + height of the image
    """
    all_x, all_y = zip(*polygon)
    x, y = min(all_x), min(all_y)
    width, height = max(all_x) - x, max(all_y) - y
    return ",".join(list(map(str, [int(x), int(y), int(width), int(height)])))
