# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
"""
Each transform class defined here takes as input a PIL Image and returns the modified PIL Image
"""
from enum import Enum
from random import randint

import albumentations as A
import cv2
import numpy as np
from albumentations.augmentations import (
    Affine,
    CoarseDropout,
    ColorJitter,
    ElasticTransform,
    GaussianBlur,
    GaussNoise,
    Perspective,
    RandomScale,
    Sharpen,
    ToGray,
)
from albumentations.core.transforms_interface import ImageOnlyTransform
from cv2 import dilate, erode
from numpy import random
from torch import Tensor
from torchvision.transforms import Compose, ToPILImage
from torchvision.transforms.functional import resize


class Preprocessing(str, Enum):
    MaxResize = "max_resize"
    """
    If the image is bigger than the given size, resize it while keeping the original ratio
    """

    FixedHeightResize = "fixed_height_resize"
    """
    Resize the height to a fixed value while keeping the original ratio
    """

    FixedWidthResize = "fixed_width_resize"
    """
    Resize the width to a fixed value while keeping the original ratio
    """

    FixedResize = "fixed_resize"
    """
    Resize both the width and the height to a fixed value
    """


class FixedHeightResize:
    """
    Resize an image tensor to a fixed height
    """

    def __init__(self, height: int) -> None:
        self.height = height

    def __call__(self, img: Tensor) -> Tensor:
        size = (self.height, self._calc_new_width(img))
        return resize(img, size, antialias=False)

    def _calc_new_width(self, img: Tensor) -> int:
        aspect_ratio = img.shape[2] / img.shape[1]
        return round(self.height * aspect_ratio)


class FixedWidthResize:
    """
    Resize an image tensor to a fixed width
    """

    def __init__(self, width: int) -> None:
        self.width = width

    def __call__(self, img: Tensor) -> Tensor:
        size = (self._calc_new_height(img), self.width)
        return resize(img, size, antialias=False)

    def _calc_new_height(self, img: Tensor) -> int:
        aspect_ratio = img.shape[1] / img.shape[2]
        return round(self.width * aspect_ratio)


class FixedResize:
    """
    Resize an image tensor to a fixed width and height
    """

    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width

    def __call__(self, img: Tensor) -> Tensor:
        return resize(img, (self.height, self.width), antialias=False)


class MaxResize:
    """
    Resize an image tensor if it is bigger than the maximum size
    """

    def __init__(self, height: int, width: int) -> None:
        self.max_width = width
        self.max_height = height

    def __call__(self, img: Tensor) -> Tensor:
        height, width = img.shape[1:]
        if width <= self.max_width and height <= self.max_height:
            return img
        width_ratio = self.max_width / width
        height_ratio = self.max_height / height
        ratio = min(height_ratio, width_ratio)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return resize(img, (new_height, new_width), antialias=False)


class Dilation:
    """
    OCR: stroke width increasing
    """

    def __init__(self, kernel, iterations):
        self.kernel = kernel
        self.iterations = iterations

    def __call__(self, x):
        return dilate(np.array(x), self.kernel, iterations=self.iterations)


class Erosion:
    """
    OCR: stroke width decreasing
    """

    def __init__(self, kernel, iterations):
        self.kernel = kernel
        self.iterations = iterations

    def __call__(self, x):
        return erode(np.array(x), self.kernel, iterations=self.iterations)


class ErosionDilation(ImageOnlyTransform):
    """
    Random erosion or dilation
    """

    def __init__(
        self,
        min_kernel: int,
        max_kernel: int,
        iterations: int,
        always_apply: bool = False,
        p: float = 1.0,
    ):
        super(ErosionDilation, self).__init__(always_apply, p)
        self.min_kernel = min_kernel
        self.max_kernel = max_kernel
        self.iterations = iterations
        self.p = p
        self.always_apply = False

    def apply(self, img: np.ndarray, **params):
        kernel_h = randint(self.min_kernel, self.max_kernel)
        kernel_w = randint(self.min_kernel, self.max_kernel)
        kernel = np.ones((kernel_h, kernel_w), np.uint8)
        return (
            Erosion(kernel, iterations=self.iterations)(img)
            if random.random() < 0.5
            else Dilation(kernel=kernel, iterations=self.iterations)(img)
        )


def get_preprocessing_transforms(
    preprocessings: list, to_pil_image: bool = False
) -> Compose:
    """
    Returns a list of transformations to be applied to the image.
    """
    transforms = []
    for preprocessing in preprocessings:
        match preprocessing["type"]:
            case Preprocessing.MaxResize:
                transforms.append(
                    MaxResize(
                        height=preprocessing["max_height"],
                        width=preprocessing["max_width"],
                    )
                )
            case Preprocessing.FixedHeightResize:
                transforms.append(
                    FixedHeightResize(height=preprocessing["fixed_height"])
                )
            case Preprocessing.FixedWidthResize:
                transforms.append(FixedWidthResize(width=preprocessing["fixed_width"]))
            case Preprocessing.FixedResize:
                transforms.append(
                    FixedResize(
                        height=preprocessing["fixed_height"],
                        width=preprocessing["fixed_width"],
                    )
                )
    if to_pil_image:
        transforms.append(ToPILImage())
    return Compose(transforms)


def get_augmentation_transforms() -> A.Compose:
    """
    Returns a list of transformation to be applied to the image.
    """
    return A.Compose(
        [
            # Scale between 0.75 and 1.0
            RandomScale(
                scale_limit=[-0.25, 0], always_apply=True, interpolation=cv2.INTER_AREA
            ),
            A.SomeOf(
                [
                    ErosionDilation(min_kernel=1, max_kernel=4, iterations=1),
                    Perspective(scale=(0.05, 0.09), fit_output=True, p=0.4),
                    GaussianBlur(sigma_limit=2.5, p=1),
                    GaussNoise(var_limit=50**2, p=1),
                    ColorJitter(
                        contrast=0.2,
                        brightness=0.2,
                        saturation=0.2,
                        hue=0.2,
                        p=1,
                    ),
                    ElasticTransform(
                        alpha=20.0,
                        sigma=5.0,
                        alpha_affine=1.0,
                        border_mode=0,
                        p=1,
                    ),
                    Sharpen(alpha=(0.0, 1.0), p=1),
                    Affine(shear={"x": (-20, 20), "y": (0, 0)}, p=1),
                    CoarseDropout(p=1),
                    ToGray(p=0.5),
                ],
                n=2,
                p=0.9,
            ),
        ],
        p=0.9,
    )
