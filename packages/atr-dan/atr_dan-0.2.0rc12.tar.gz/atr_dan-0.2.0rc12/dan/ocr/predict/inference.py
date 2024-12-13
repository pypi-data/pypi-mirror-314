# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

import json
import logging
import pickle
import re
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
import yaml

from dan.ocr.decoder import CTCLanguageDecoder, GlobalHTADecoder
from dan.ocr.encoder import FCN_Encoder
from dan.ocr.predict.attention import (
    Level,
    get_predicted_polygons_with_confidence,
    parse_delimiters,
    plot_attention,
    split_text_and_confidences,
)
from dan.ocr.transforms import get_preprocessing_transforms
from dan.ocr.utils import load_font
from dan.utils import (
    EntityType,
    ind_to_token,
    list_to_batches,
    pad_images,
    parse_charset_pattern,
    parse_tokens_pattern,
    read_image,
)

logger = logging.getLogger(__name__)


class DAN:
    """
    The DAN class is used to apply a DAN model.
    The class initializes useful parameters: the device and the temperature scalar parameter.
    """

    def __init__(self, device: str, temperature=1.0) -> None:
        """
        Constructor of the DAN class.
        :param device: The device to use.
        """
        super(DAN, self).__init__()
        self.device = device
        self.temperature = temperature

    def load(
        self,
        path: Path,
        mode: str = "eval",
        use_language_model: bool = False,
        compile_model: bool = False,
        dynamic_mode: bool = False,
    ) -> None:
        """
        Load a trained model.
        :param path: Path to the directory containing the model, the YAML parameters file and the charset file.
        :param mode: The mode to load the model (train or eval).
        :param use_language_model: Whether to use an explicit language model to rescore text hypotheses.
        :param compile_model: Whether to compile the model.
        :param dynamic_mode: Whether to use the dynamic mode during model compilation.
        """
        model_path = path / "model.pt"
        assert model_path.is_file(), f"File {model_path} not found"

        params_path = path / "parameters.yml"
        assert params_path.is_file(), f"File {params_path} not found"

        charset_path = path / "charset.pkl"
        assert charset_path.is_file(), f"File {charset_path} not found"

        parameters = yaml.safe_load(params_path.read_text())["parameters"]
        parameters["decoder"]["device"] = self.device

        self.charset = sorted(pickle.loads(charset_path.read_bytes()))

        # Restore the model weights.
        checkpoint = torch.load(model_path, map_location=self.device)

        encoder = FCN_Encoder(parameters["encoder"]).to(self.device)
        encoder.load_state_dict(checkpoint["encoder_state_dict"], strict=True)

        decoder = GlobalHTADecoder(parameters["decoder"]).to(self.device)
        decoder.load_state_dict(checkpoint["decoder_state_dict"], strict=True)

        logger.debug(f"Loaded model {model_path}")

        if compile_model:
            torch.compiler.cudagraph_mark_step_begin()
            encoder = torch.compile(encoder, dynamic=True if dynamic_mode else None)

            torch.compiler.cudagraph_mark_step_begin()
            decoder = torch.compile(decoder, dynamic=True if dynamic_mode else None)

            logger.info("Encoder and decoder have been compiled")

        if mode == "train":
            encoder.train()
            decoder.train()
        elif mode == "eval":
            encoder.eval()
            decoder.eval()
        else:
            raise Exception("Unsupported mode")

        self.encoder = encoder
        self.decoder = decoder
        self.lm_decoder = None

        if use_language_model and parameters["language_model"]["weight"] > 0:
            logger.info(
                f"Decoding with a language model (weight={parameters['language_model']['weight']})."
            )
            self.lm_decoder = CTCLanguageDecoder(
                language_model_path=parameters["language_model"]["model"],
                lexicon_path=parameters["language_model"]["lexicon"],
                tokens_path=parameters["language_model"]["tokens"],
                language_model_weight=parameters["language_model"]["weight"],
            )

        self.mean, self.std = (
            torch.tensor(parameters["mean"]) / 255 if "mean" in parameters else None,
            torch.tensor(parameters["std"]) / 255 if "std" in parameters else None,
        )
        self.preprocessing_transforms = get_preprocessing_transforms(
            parameters.get("preprocessings", [])
        )
        self.max_chars = parameters["max_char_prediction"]

    @property
    def use_lm(self) -> bool:
        """
        Whether the model decodes with a Language Model
        """
        return self.lm_decoder is not None

    def preprocess(self, path: str) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Preprocess an image.
        :param path: Path of the image to load and preprocess.
        """
        image = read_image(path)
        preprocessed_image = self.preprocessing_transforms(image)

        if self.mean is None and self.std is None:
            return preprocessed_image, preprocessed_image

        size = preprocessed_image.shape
        normalized_image = torch.zeros(size)

        mean = self.mean if self.mean is not None else torch.zeros(size[0])
        std = self.std if self.std is not None else torch.ones(size[0])

        for ch in range(size[0]):
            normalized_image[ch, :, :] = (
                preprocessed_image[ch, :, :] - mean[ch]
            ) / std[ch]

        return preprocessed_image, normalized_image

    def predict(
        self,
        input_tensor: torch.Tensor,
        input_sizes: List[torch.Size],
        char_separators: re.Pattern,
        confidences: bool = False,
        attentions: bool = False,
        attention_level: Level = Level.Line,
        extract_objects: bool = False,
        word_separators: re.Pattern = parse_delimiters(["\n", " "]),
        line_separators: re.Pattern = parse_delimiters(["\n"]),
        tokens_separators: re.Pattern | None = None,
        start_token: str | None = None,
        max_object_height: int = 50,
    ) -> dict:
        """
        Run prediction on an input image.
        :param input_tensor: A batch of images to predict.
        :param input_sizes: The original images sizes.
        :param char_separators: The regular expression pattern to split characters.
        :param confidences: Return the characters probabilities.
        :param attentions: Return characters attention weights.
        :param attention_level: Level of text pieces (must be in [char, word, line, ner])
        :param extract_objects: Whether to extract polygons' coordinates.
        :param word_separators: The regular expression pattern to split words.
        :param line_separators: The regular expression pattern to split lines.
        :param tokens_separators: The regular expression pattern to split NER tokens.
        :param start_token: The starting token for the prediction.
        :param max_object_height: Maximum height of predicted objects.
        """
        input_tensor = input_tensor.to(self.device)

        start_token = (
            self.charset.index(start_token) if start_token else len(self.charset) + 1
        )
        end_token = len(self.charset)

        # Run the prediction.
        with torch.no_grad():
            batch_size = input_tensor.size(0)
            reached_end = torch.zeros(
                (batch_size,), dtype=torch.bool, device=self.device
            )
            prediction_len = torch.zeros(
                (batch_size,), dtype=torch.int, device=self.device
            )
            predicted_tokens = (
                torch.ones((batch_size, 1), dtype=torch.long, device=self.device)
                * start_token
            )
            predicted_tokens_len = torch.ones(
                (batch_size,), dtype=torch.int, device=self.device
            )

            # end token index will be used for ctc
            tot_pred = torch.zeros(
                (batch_size, len(self.charset) + 1, self.max_chars),
                dtype=torch.float,
                device=self.device,
            )

            whole_output = list()
            confidence_scores = list()
            attention_maps = list()
            cache = None
            hidden_predict = None

            features = self.encoder(input_tensor.float())
            features_size = features.size()
            features = self.decoder.features_updater.get_pos_features(features)
            features = torch.flatten(features, start_dim=2, end_dim=3).permute(2, 0, 1)

            for i in range(0, self.max_chars):
                (
                    output,
                    pred,
                    hidden_predict,
                    cache,
                    weights,
                ) = self.decoder(
                    features,
                    predicted_tokens,
                    input_sizes,
                    predicted_tokens_len.tolist(),
                    features_size,
                    start=0,
                    hidden_predict=hidden_predict,
                    cache=cache,
                    num_pred=1,
                )

                # output total logit prediction
                tot_pred[:, :, i : i + 1] = pred

                pred = pred / self.temperature
                whole_output.append(output)
                attention_maps.append(weights)
                confidence_scores.append(
                    torch.max(torch.softmax(pred[:, :], dim=1), dim=1).values
                )
                predicted_tokens = torch.cat(
                    [
                        predicted_tokens,
                        torch.argmax(pred[:, :, -1], dim=1, keepdim=True),
                    ],
                    dim=1,
                )
                reached_end = torch.logical_or(
                    reached_end, torch.eq(predicted_tokens[:, -1], end_token)
                )
                predicted_tokens_len += 1

                prediction_len[reached_end == False] = i + 1  # noqa E712

                if torch.all(reached_end):
                    break

            # Concatenate tensors for each token
            confidence_scores = (
                torch.cat(confidence_scores, dim=1).cpu().detach().numpy()
            )
            attention_maps = torch.cat(attention_maps, dim=1).cpu().detach().numpy()

            # Remove bot and eot tokens
            predicted_tokens = predicted_tokens[:, 1:]
            prediction_len[torch.eq(reached_end, False)] = self.max_chars - 1
            predicted_tokens = [
                predicted_tokens[i, : prediction_len[i]] for i in range(batch_size)
            ]
            confidence_scores = [
                confidence_scores[i, : prediction_len[i]].tolist()
                for i in range(batch_size)
            ]

            # Transform tokens to characters
            predicted_text = [
                ind_to_token(self.charset, t, oov_symbol="") for t in predicted_tokens
            ]

            logger.info("Images processed")

        out = {}

        out["text"] = predicted_text
        if self.use_lm:
            out["language_model"] = self.lm_decoder(tot_pred, prediction_len)
        if confidences:
            out["confidences"] = confidence_scores
        if attentions:
            out["attentions"] = attention_maps
        if extract_objects:
            out["objects"] = [
                get_predicted_polygons_with_confidence(
                    predicted_text[i],
                    attention_maps[i],
                    confidence_scores[i],
                    attention_level,
                    input_sizes[i][0],
                    input_sizes[i][1],
                    max_object_height=max_object_height,
                    char_separators=char_separators,
                    word_separators=word_separators,
                    line_separators=line_separators,
                    tokens_separators=tokens_separators,
                )
                for i in range(batch_size)
            ]
        return out


def process_batch(
    image_batch: List[Path],
    dan_model: DAN,
    device: str,
    output: Path,
    confidence_score: bool,
    confidence_score_levels: List[Level],
    attention_map: bool,
    attention_map_level: Level,
    attention_map_scale: float,
    alpha_factor: int | float,
    color_map: str,
    word_separators: List[str],
    line_separators: List[str],
    predict_objects: bool,
    max_object_height: int,
    tokens: Dict[str, EntityType],
    start_token: str,
    font: Path | None = None,
    maximum_font_size: int | None = None,
) -> None:
    input_images, visu_images, input_sizes = [], [], []
    logger.info("Loading images...")
    for image_path in image_batch:
        # Load image and pre-process it
        visu_image, input_image = dan_model.preprocess(str(image_path))
        input_images.append(input_image)
        visu_images.append(visu_image)
        input_sizes.append(input_image.shape[1:])

    # Convert to tensor of size (batch_size, channel, height, width) with batch_size=1
    input_tensor = pad_images(input_images).to(device)
    visu_tensor = pad_images(visu_images).to(device)
    logger.info("Images preprocessed!")

    # Parse delimiters to regex
    char_separators = parse_charset_pattern(dan_model.charset)
    word_separators = parse_delimiters(word_separators)
    line_separators = parse_delimiters(line_separators)

    # NER Entities separators
    ner_separators = parse_tokens_pattern(tokens.values()) if tokens else None
    # Predict
    logger.info("Predicting...")
    prediction = dan_model.predict(
        input_tensor,
        input_sizes,
        confidences=confidence_score,
        attentions=attention_map,
        attention_level=attention_map_level,
        extract_objects=predict_objects,
        char_separators=char_separators,
        word_separators=word_separators,
        line_separators=line_separators,
        tokens_separators=ner_separators,
        max_object_height=max_object_height,
        start_token=start_token,
    )

    logger.info("Prediction parsing...")
    for idx, image_path in enumerate(image_batch):
        predicted_text = prediction["text"][idx]
        result = {"text": predicted_text, "confidences": {}, "language_model": {}}

        if predicted_text:
            # Return LM results
            if dan_model.use_lm:
                result["language_model"] = {
                    "text": prediction["language_model"]["text"][idx],
                    "confidence": prediction["language_model"]["confidence"][idx],
                }

            # Return extracted objects (coordinates, text, confidence)
            if predict_objects:
                result["objects"] = prediction["objects"][idx]

            # Return mean confidence score
            if confidence_score:
                char_confidences = prediction["confidences"][idx]
                result["confidences"]["total"] = np.around(np.mean(char_confidences), 2)

                for level in confidence_score_levels:
                    result["confidences"][level.value] = []
                    texts, confidences, _ = split_text_and_confidences(
                        predicted_text,
                        char_confidences,
                        level,
                        char_separators,
                        word_separators,
                        line_separators,
                        ner_separators,
                    )

                    for text, conf in zip(texts, confidences):
                        result["confidences"][level.value].append(
                            {"text": text, "confidence": conf}
                        )

            # Save gif with attention map
            if attention_map and font and maximum_font_size:
                attentions = prediction["attentions"][idx]
                gif_filename = (
                    f"{output}/{image_path.stem}_{attention_map_level.value}.gif"
                )
                logger.info(f"Creating attention GIF in {gif_filename}")
                plot_attention(
                    image=visu_tensor[idx],
                    text=predicted_text,
                    weights=attentions,
                    level=attention_map_level,
                    scale=attention_map_scale,
                    alpha_factor=alpha_factor,
                    color_map=color_map,
                    char_separators=char_separators,
                    word_separators=word_separators,
                    line_separators=line_separators,
                    tokens_separators=ner_separators,
                    display_polygons=predict_objects,
                    max_object_height=max_object_height,
                    outname=gif_filename,
                    font=font,
                    maximum_font_size=maximum_font_size,
                )
                result["attention_gif"] = gif_filename

        json_filename = Path(output, f"{image_path.stem}.json")
        logger.info(f"Saving JSON prediction in {json_filename}")
        json_filename.write_text(json.dumps(result, indent=2))


def run(
    image_dir: Path,
    model: Path,
    font: Path,
    maximum_font_size: int,
    output: Path,
    confidence_score: bool,
    confidence_score_levels: List[Level],
    attention_map: bool,
    attention_map_level: Level,
    attention_map_scale: float,
    alpha_factor: int | float,
    color_map: str,
    word_separators: List[str],
    line_separators: List[str],
    temperature: float,
    predict_objects: bool,
    max_object_height: int,
    image_extension: str,
    gpu_device: int,
    batch_size: int,
    tokens: Dict[str, EntityType],
    start_token: str,
    use_language_model: bool,
    compile_model: bool,
    dynamic_mode: bool,
) -> None:
    """
    Predict a single image save the output
    :param image_dir: Path to the folder where the images to predict are stored.
    :param model: Path to the directory containing the model, the YAML parameters file and the charset file to use for prediction.
    :param font: Path to the font file to use for the GIF of the attention map.
    :param maximum_font_size: Maximum font size to use for the GIF of the attention map.
    :param output: Path to the output folder where the results will be saved.
    :param confidence_score: Whether to compute confidence score.
    :param confidence_score_levels: Levels of objects to extract.
    :param attention_map: Whether to plot the attention map.
    :param attention_map_level: Level of objects to extract.
    :param attention_map_scale: Scaling factor for the attention map.
    :param alpha_factor: Alpha factor for the attention map.
    :param color_map: A matplotlib colormap to use for the attention maps.
    :param word_separators: List of word separators.
    :param line_separators: List of line separators.
    :param temperature: Temperature scalar parameter.
    :param predict_objects: Whether to extract objects.
    :param max_object_height: Maximum height of predicted objects.
    :param image_extension: Extension of the images to predict.
    :param gpu_device: Use a specific GPU if available.
    :param batch_size: Size of the batches for prediction.
    :param tokens: NER tokens used.
    :param start_token: Use a specific starting token at the beginning of the prediction. Useful when making predictions on different single pages.
    :param use_language_model: Whether to use an explicit language model to rescore text hypotheses.
    :param compile_model: Whether to compile the model.
    :param dynamic_mode: Whether to use the dynamic mode during model compilation.
    """
    # Create output directory if necessary
    if not output.exists():
        output.mkdir()

    # Load model
    cuda_device = f":{gpu_device}" if gpu_device is not None else ""
    device = f"cuda{cuda_device}" if torch.cuda.is_available() else "cpu"
    dan_model = DAN(device, temperature)
    dan_model.load(
        model,
        mode="eval",
        use_language_model=use_language_model,
        compile_model=compile_model,
        dynamic_mode=dynamic_mode,
    )

    # Load font if the attention map is drawn
    if attention_map:
        try:
            load_font(font, maximum_font_size)
        except OSError:
            raise FileNotFoundError(f"The font file is missing at path `{str(font)}`")

    images = image_dir.rglob(f"*{image_extension}")
    for image_batch in list_to_batches(images, n=batch_size):
        process_batch(
            image_batch,
            dan_model,
            device,
            output,
            confidence_score,
            confidence_score_levels,
            attention_map,
            attention_map_level,
            attention_map_scale,
            alpha_factor,
            color_map,
            word_separators,
            line_separators,
            predict_objects,
            max_object_height,
            tokens,
            start_token,
            font,
            maximum_font_size,
        )
