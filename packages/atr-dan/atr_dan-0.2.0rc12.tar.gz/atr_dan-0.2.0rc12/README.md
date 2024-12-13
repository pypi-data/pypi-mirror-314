# DAN: a Segmentation-free Document Attention Network for Handwritten Document Recognition

[![Python >= 3.10](https://img.shields.io/badge/Python-%3E%3D3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

For more details about this package, make sure to see the documentation available at <https://atr.pages.teklia.com/dan/>.

This is an open-source project, licensed using [the CeCILL-C license](https://cecill.info/index.en.html).

## Inference

To apply DAN to an image, one needs to first add a few imports and to load an image. Note that the image should be in RGB.

```python
import cv2
from dan.ocr.predict.inference import DAN

image = cv2.cvtColor(cv2.imread(IMAGE_PATH), cv2.COLOR_BGR2RGB)
```

Then one can initialize and load the trained model with the parameters used during training. The directory passed as parameter should have:

- a `model.pt` file,
- a `charset.pkl` file,
- a `parameters.yml` file corresponding to the `inference_parameters.yml` file generated during training.

```python
from pathlib import Path

model_path = Path("models")

model = DAN("cpu")
model.load(model_path, mode="eval")
```

To run the inference on a GPU, one can replace `cpu` by the name of the GPU. In the end, one can run the prediction:

```python
from pathlib import Path
from dan.utils import parse_charset_pattern

# Load image
image_path = "images/page.jpg"
_, image = dan_model.preprocess(str(image_path))

input_tensor = image.unsqueeze(0)
input_tensor = input_tensor.to("cpu")
input_sizes = [image.shape[1:]]

# Predict
text, confidence_scores = model.predict(
    input_tensor,
    input_sizes,
    char_separators=parse_charset_pattern(dan_model.charset),
    confidences=True,
)
```

## Training

This package provides three subcommands. To get more information about any subcommand, use the `--help` option.

### Get started

See the [dedicated page](https://atr.pages.teklia.com/dan/get_started/training/) on the official DAN documentation.

### Data extraction from Arkindex

See the [dedicated page](https://atr.pages.teklia.com/dan/usage/datasets/extract/) on the official DAN documentation.

### Model training

See the [dedicated page](https://atr.pages.teklia.com/dan/usage/train/) on the official DAN documentation.

### Model prediction

See the [dedicated page](https://atr.pages.teklia.com/dan/usage/predict/) on the official DAN documentation.
