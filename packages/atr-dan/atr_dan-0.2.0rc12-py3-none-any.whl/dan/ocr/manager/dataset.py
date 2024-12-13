# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import copy
import json

import numpy as np
from torch.utils.data import Dataset
from tqdm import tqdm

from dan.datasets.utils import natural_sort
from dan.utils import read_image, token_to_ind


class OCRDataset(Dataset):
    """
    Dataset class to handle dataset loading
    """

    def __init__(
        self,
        set_name,
        paths_and_sets,
        charset,
        tokens,
        preprocessing_transforms,
        augmentation_transforms,
        load_in_memory=False,
        mean=None,
        std=None,
    ):
        self.set_name = set_name
        self.charset = charset
        self.tokens = tokens
        self.load_in_memory = load_in_memory
        self.mean = mean
        self.std = std

        # Pre-processing, augmentation
        self.preprocessing_transforms = preprocessing_transforms
        self.augmentation_transforms = augmentation_transforms

        # Factor to reduce the height and width of the feature vector before feeding the decoder.
        self.reduce_dims_factor = np.array([32, 8, 1])

        # Load samples and preprocess images if load_in_memory is True
        self.samples = self.load_samples(paths_and_sets)

        # Curriculum config
        self.curriculum_config = None

    def __len__(self):
        """
        Return the dataset size
        """
        return len(self.samples)

    def __getitem__(self, idx):
        """
        Return an item from the dataset (image and label)
        """
        # Load preprocessed image
        sample = copy.deepcopy(self.samples[idx])
        if not self.load_in_memory:
            sample["img"] = self.get_sample_img(idx)

        # Convert to numpy
        sample["img"] = np.array(sample["img"])

        # Apply data augmentation
        if self.augmentation_transforms:
            sample["img"] = self.augmentation_transforms(image=sample["img"])["image"]

        # Image normalization
        sample["img"] = (sample["img"] - self.mean) / self.std

        # Get final height and width
        sample["img_reduced_shape"], sample["img_position"] = self.compute_final_size(
            sample["img"]
        )

        # Convert label into tokens
        sample["token_label"], sample["label_len"] = self.convert_sample_label(
            sample["label"]
        )
        return sample

    def load_samples(self, paths_and_sets):
        """
        Load images and labels
        """
        samples = list()

        for path_and_set in paths_and_sets:
            path = path_and_set["path"]
            gt_per_set = json.loads((path / "labels.json").read_text())
            set_name = path_and_set["set_name"]
            gt = gt_per_set[set_name]
            for filename in natural_sort(gt):
                filepath = path / filename
                samples.append(
                    {
                        "name": filepath.name,
                        "label": gt[filename],
                        "path": filepath.resolve(),
                    }
                )
                if self.load_in_memory:
                    samples[-1]["img"] = self.preprocessing_transforms(
                        read_image(str(filepath))
                    )
        return samples

    def get_sample_img(self, i):
        """
        Get image by index
        """
        if self.load_in_memory:
            return self.samples[i]["img"]

        image_path = str(self.samples[i]["path"])
        return self.preprocessing_transforms(read_image(image_path))

    def compute_std_mean(self):
        """
        Compute cumulated variance and mean of whole dataset
        """
        if self.mean is not None and self.std is not None:
            return self.mean, self.std

        total = np.zeros((3,))
        diff = np.zeros((3,))
        nb_pixels = 0
        for metric in ["mean", "std"]:
            for ind in tqdm(range(len(self.samples)), desc=f"Computing {metric} value"):
                img = np.array(self.get_sample_img(ind))
                if metric == "mean":
                    total += np.sum(img, axis=(0, 1))
                    nb_pixels += np.prod(img.shape[:2])
                elif metric == "std":
                    diff += [
                        np.sum((img[:, :, k] - self.mean[k]) ** 2) for k in range(3)
                    ]
            if metric == "mean":
                self.mean = total / nb_pixels
            elif metric == "std":
                self.std = np.sqrt(diff / nb_pixels)
        return self.mean, self.std

    def compute_final_size(self, img):
        """
        Compute the final image size and position after feature extraction
        """
        image_reduced_shape = np.ceil(img.shape / self.reduce_dims_factor).astype(int)

        if self.set_name == "train":
            image_reduced_shape = [max(1, t) for t in image_reduced_shape]

        image_position = [
            [0, img.shape[0]],
            [0, img.shape[1]],
        ]
        return image_reduced_shape, image_position

    def convert_sample_label(self, label):
        """
        Tokenize the label and return its length
        """
        token_label = token_to_ind(self.charset, label)
        token_label.append(self.tokens["end"])
        label_len = len(token_label)
        token_label.insert(0, self.tokens["start"])
        return token_label, label_len
