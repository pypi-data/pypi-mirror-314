import functools
import os
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

import wandb

if TYPE_CHECKING:
    from wandb.sdk.data_types.image import ImageDataOrPathType


WANDB_AVAILABLE = False


class Config(str, Enum):
    ANALYZE = "analyze"
    TRAINING = "training"
    EVALUATION = "evaluation"

    def __str__(self):
        return self.value


def wandb_required(func):
    """
    Always check that "Weights & Biases" is available before executing the function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not WANDB_AVAILABLE:
            return
        return func(*args, **kwargs)

    return wrapper


def init(wandb_params: dict | None, config: dict, output_folder: Path) -> None:
    if not wandb_params:
        return

    # Store "Weights & Biases" files in the output folder by default
    if not os.getenv("WANDB_DIR"):
        os.environ["WANDB_DIR"] = str(output_folder)
    # Path should already exist when "Weights & Biases" is instantiated
    Path(os.environ["WANDB_DIR"]).mkdir(parents=True, exist_ok=True)

    # Update config to log
    wandb_config = wandb_params.get("config", {})

    forbidden_keys = set(wandb_config.keys()).intersection(list(map(str, Config)))
    assert (
        not forbidden_keys
    ), f"Keys {list(forbidden_keys)} are forbidden in W&B config"

    wandb_params = wandb_params.copy()  # Avoid recursions
    wandb_params["config"] = {**config, **wandb_config}

    wandb.init(**wandb_params)

    global WANDB_AVAILABLE
    WANDB_AVAILABLE = True


@wandb_required
def log(*args, **kwargs) -> None:
    wandb.log(*args, **kwargs)


@wandb_required
def image(image_name: str, image_data: "ImageDataOrPathType", *args, **kwargs) -> None:
    image = wandb.Image(image_data)
    log(data={image_name: image}, *args, **kwargs)


@wandb_required
def table(table_name: str, *args, **kwargs) -> None:
    table = wandb.Table(*args, **kwargs)
    log(data={table_name: table}, commit=True)


@wandb_required
def artifact(*args, **kwargs) -> wandb.Artifact | None:
    return wandb.Artifact(*args, **kwargs)


@wandb_required
def log_artifact(artifact: wandb.Artifact, *args, **kwargs) -> None:
    artifact.add_file(*args, **kwargs)
    wandb.log_artifact(artifact)


@wandb_required
def run_id() -> str | None:
    if not wandb.run:
        return

    return wandb.run.id
