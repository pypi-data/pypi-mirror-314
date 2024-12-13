# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-
import pickle
import random

import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler

from dan.ocr.manager.dataset import OCRDataset
from dan.ocr.transforms import get_augmentation_transforms, get_preprocessing_transforms
from dan.utils import pad_images, pad_sequences_1D


class OCRDatasetManager:
    def __init__(
        self, dataset_params: dict, training_params: dict, device: torch.device
    ):
        self.params = dataset_params
        self.training_params = training_params
        self.device_params = training_params["device"]

        # Whether data should be copied on GPU via https://pytorch.org/docs/stable/generated/torch.Tensor.pin_memory.html
        self.pin_memory = device != torch.device("cpu")

        self.train_dataset = None
        self.valid_datasets = dict()
        self.test_datasets = dict()

        self.train_loader = None
        self.valid_loaders = dict()
        self.test_loaders = dict()

        self.train_sampler = None
        self.valid_samplers = dict()
        self.test_samplers = dict()

        self.mean = None
        self.std = None

        self.generator = torch.Generator()
        self.generator.manual_seed(0)

        self.load_in_memory = self.training_params["data"].get("load_in_memory", True)
        self.charset = self.get_charset()
        self.tokens = self.get_tokens()
        self.training_params["data"]["padding_token"] = self.tokens["pad"]

        self.my_collate_function = OCRCollateFunction(
            padding_token=training_params["data"]["padding_token"]
        )
        self.augmentation = (
            get_augmentation_transforms()
            if self.training_params["data"]["augmentation"]
            else None
        )
        self.preprocessing = get_preprocessing_transforms(
            training_params["data"]["preprocessings"], to_pil_image=True
        )

    def load_datasets(self):
        """
        Load training and validation datasets
        """
        self.train_dataset = OCRDataset(
            set_name="train",
            paths_and_sets=self.get_paths_and_sets(self.params["train"]["datasets"]),
            charset=self.charset,
            tokens=self.tokens,
            preprocessing_transforms=self.preprocessing,
            augmentation_transforms=self.augmentation,
            load_in_memory=self.load_in_memory,
            mean=self.mean,
            std=self.std,
        )

        self.mean, self.std = self.train_dataset.compute_std_mean()

        for custom_name in self.params["val"]:
            self.valid_datasets[custom_name] = OCRDataset(
                set_name="val",
                paths_and_sets=self.get_paths_and_sets(self.params["val"][custom_name]),
                charset=self.charset,
                tokens=self.tokens,
                preprocessing_transforms=self.preprocessing,
                augmentation_transforms=None,
                load_in_memory=self.load_in_memory,
                mean=self.mean,
                std=self.std,
            )

    def load_ddp_samplers(self):
        """
        Load training and validation data samplers
        """
        if self.device_params["use_ddp"]:
            self.train_sampler = DistributedSampler(
                self.train_dataset,
                num_replicas=self.device_params["nb_gpu"],
                rank=self.device_params["ddp_rank"],
                shuffle=True,
            )
            for custom_name in self.valid_datasets:
                self.valid_samplers[custom_name] = DistributedSampler(
                    self.valid_datasets[custom_name],
                    num_replicas=self.device_params["nb_gpu"],
                    rank=self.device_params["ddp_rank"],
                    shuffle=False,
                )
        else:
            for custom_name in self.valid_datasets:
                self.valid_samplers[custom_name] = None

    def load_dataloaders(self):
        """
        Load training and validation data loaders
        """
        self.train_loader = DataLoader(
            self.train_dataset,
            batch_size=self.training_params["data"]["batch_size"],
            shuffle=True if self.train_sampler is None else False,
            drop_last=False,
            sampler=self.train_sampler,
            num_workers=self.device_params["nb_gpu"]
            * self.training_params["data"]["worker_per_gpu"],
            pin_memory=self.pin_memory,
            collate_fn=self.my_collate_function,
            worker_init_fn=self.seed_worker,
            generator=self.generator,
        )

        for key in self.valid_datasets:
            self.valid_loaders[key] = DataLoader(
                self.valid_datasets[key],
                batch_size=1,
                sampler=self.valid_samplers[key],
                shuffle=False,
                num_workers=self.device_params["nb_gpu"]
                * self.training_params["data"]["worker_per_gpu"],
                pin_memory=self.pin_memory,
                drop_last=False,
                collate_fn=self.my_collate_function,
                worker_init_fn=self.seed_worker,
                generator=self.generator,
            )

    @staticmethod
    def seed_worker(worker_id):
        """
        Set worker seed
        """
        worker_seed = torch.initial_seed() % 2**32
        np.random.seed(worker_seed)
        random.seed(worker_seed)

    def generate_test_loader(self, custom_name, sets_list):
        """
        Load test dataset, data sampler and data loader
        """
        if custom_name in self.test_loaders:
            return
        paths_and_sets = list()
        for set_info in sets_list:
            paths_and_sets.append(
                {"path": self.params["datasets"][set_info[0]], "set_name": set_info[1]}
            )
        self.test_datasets[custom_name] = OCRDataset(
            set_name="test",
            paths_and_sets=paths_and_sets,
            charset=self.charset,
            tokens=self.tokens,
            preprocessing_transforms=self.preprocessing,
            augmentation_transforms=None,
            load_in_memory=self.load_in_memory,
            mean=self.mean,
            std=self.std,
        )

        if self.device_params["use_ddp"]:
            self.test_samplers[custom_name] = DistributedSampler(
                self.test_datasets[custom_name],
                num_replicas=self.device_params["nb_gpu"],
                rank=self.device_params["ddp_rank"],
                shuffle=False,
            )
        else:
            self.test_samplers[custom_name] = None

        self.test_loaders[custom_name] = DataLoader(
            self.test_datasets[custom_name],
            batch_size=1,
            sampler=self.test_samplers[custom_name],
            shuffle=False,
            num_workers=self.device_params["nb_gpu"]
            * self.training_params["data"]["worker_per_gpu"],
            pin_memory=self.pin_memory,
            drop_last=False,
            collate_fn=self.my_collate_function,
            worker_init_fn=self.seed_worker,
            generator=self.generator,
        )

    def get_paths_and_sets(self, dataset_names_folds):
        """
        Set the right path for each data set
        """
        paths_and_sets = list()
        for dataset_name, fold in dataset_names_folds:
            path = self.params["datasets"][dataset_name]
            paths_and_sets.append({"path": path, "set_name": fold})
        return paths_and_sets

    def get_charset(self):
        """
        Merge the charset of the different datasets used
        """
        if "charset" in self.params:
            return self.params["charset"]
        datasets = self.params["datasets"]
        charset = set()
        for key in datasets:
            charset = charset.union(
                set(pickle.loads((datasets[key] / "charset.pkl").read_bytes()))
            )
        if "" in charset:
            charset.remove("")
        return sorted(list(charset))

    def get_tokens(self):
        """
        Get special tokens
        """
        return {
            "end": len(self.charset),
            "start": len(self.charset) + 1,
            "pad": len(self.charset) + 2,
        }


class OCRCollateFunction:
    """
    Merge samples data to mini-batch data for OCR task
    """

    def __init__(self, padding_token):
        self.label_padding_value = padding_token

    def __call__(self, batch_data):
        formatted_batch_data = {
            "imgs": pad_images(
                [
                    torch.from_numpy(sample["img"]).permute(2, 0, 1)
                    for sample in batch_data
                ]
            ),
            "labels": pad_sequences_1D(
                [sample["token_label"] for sample in batch_data],
                padding_value=self.label_padding_value,
            ).long(),
        }

        formatted_batch_data.update(
            {
                formatted_key: [sample[initial_key] for sample in batch_data]
                for formatted_key, initial_key in zip(
                    [
                        "names",
                        "imgs_position",
                        "imgs_reduced_shape",
                        "labels_len",
                        "raw_labels",
                    ],
                    ["name", "img_position", "img_reduced_shape", "label_len", "label"],
                )
            }
        )
        return formatted_batch_data
