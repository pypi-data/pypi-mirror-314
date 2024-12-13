# Copyright Teklia (contact@teklia.com) & Denis Coquenet
# This code is licensed under CeCILL-C

# -*- coding: utf-8 -*-

from typing import Dict, List

import numpy as np
import torch
from torch import relu, softmax
from torch.nn import Conv1d, Dropout, Embedding, LayerNorm, Linear, Module, ModuleList
from torch.nn.init import xavier_uniform_
from torchaudio.models.decoder import CTCHypothesis, ctc_decoder

from dan.utils import LMTokenMapping, read_txt


class PositionalEncoding1D(Module):
    def __init__(self, dim, len_max, device):
        super(PositionalEncoding1D, self).__init__()
        self.pe = torch.zeros((1, dim, len_max), device=device, requires_grad=False)

        div = torch.exp(
            -torch.arange(0.0, dim, 2) / dim * torch.log(torch.tensor(10000.0))
        ).unsqueeze(1)
        l_pos = torch.arange(0.0, len_max)
        self.pe[:, ::2, :] = torch.sin(l_pos * div).unsqueeze(0)
        self.pe[:, 1::2, :] = torch.cos(l_pos * div).unsqueeze(0)

    def forward(self, x, start):
        """
        Add 1D positional encoding to x
        x: (B, C, L)
        start: index for x[:,:, 0]
        """
        if isinstance(start, int):
            return x + self.pe[:, :, start : start + x.size(2)].to(x.device)
        else:
            for i in range(x.size(0)):
                x[i] = x[i] + self.pe[0, :, start[i] : start[i] + x.size(2)]
            return x


class PositionalEncoding2D(Module):
    def __init__(self, dim, h_max, w_max, device):
        super(PositionalEncoding2D, self).__init__()
        self.pe = torch.zeros(
            (1, dim, h_max, w_max), device=device, requires_grad=False
        )

        div = torch.exp(
            -torch.arange(0.0, dim // 2, 2) / dim * torch.log(torch.tensor(10000.0))
        ).unsqueeze(1)
        w_pos = torch.arange(0.0, w_max)
        h_pos = torch.arange(0.0, h_max)
        self.pe[:, : dim // 2 : 2, :, :] = (
            torch.sin(h_pos * div).unsqueeze(0).unsqueeze(3).repeat(1, 1, 1, w_max)
        )
        self.pe[:, 1 : dim // 2 : 2, :, :] = (
            torch.cos(h_pos * div).unsqueeze(0).unsqueeze(3).repeat(1, 1, 1, w_max)
        )
        self.pe[:, dim // 2 :: 2, :, :] = (
            torch.sin(w_pos * div).unsqueeze(0).unsqueeze(2).repeat(1, 1, h_max, 1)
        )
        self.pe[:, dim // 2 + 1 :: 2, :, :] = (
            torch.cos(w_pos * div).unsqueeze(0).unsqueeze(2).repeat(1, 1, h_max, 1)
        )

    def forward(self, x):
        """
        Add 2D positional encoding to x
        x: (B, C, H, W)
        """
        return x + self.pe[:, :, : x.size(2), : x.size(3)]


class CustomMultiHeadAttention(Module):
    """
    Re-implementation of Multi-head Attention
    """

    def __init__(self, embed_dim, num_heads, dropout=0, proj_value=True):
        super().__init__()

        self.proj_value = proj_value

        self.in_proj_q = Linear(embed_dim, embed_dim)
        self.in_proj_k = Linear(embed_dim, embed_dim)
        if self.proj_value:
            self.in_proj_v = Linear(embed_dim, embed_dim)
        self.out_proj = Linear(embed_dim, embed_dim)

        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.scale_factor = float(self.head_dim) ** -0.5
        self.dropout = Dropout(dropout)

    def forward(
        self,
        query,
        key,
        value,
        key_padding_mask=None,
        attn_mask=None,
        output_weights=True,
    ):
        target_len, b, c = query.size()
        source_len = key.size(0)
        q = self.in_proj_q(query)
        k = self.in_proj_k(key)
        v = self.in_proj_v(value) if self.proj_value else value
        q = q * self.scale_factor

        q = torch.reshape(q, (target_len, b * self.num_heads, self.head_dim)).transpose(
            0, 1
        )
        k = torch.reshape(k, (source_len, b * self.num_heads, self.head_dim)).transpose(
            0, 1
        )
        v = torch.reshape(v, (source_len, b * self.num_heads, self.head_dim)).transpose(
            0, 1
        )

        attn_output_weights = torch.bmm(q, k.transpose(1, 2))

        if attn_mask is not None:
            attn_mask = attn_mask.unsqueeze(0)
            if attn_mask.dtype == torch.bool:
                attn_output_weights.masked_fill_(attn_mask, float("-inf"))
            else:
                attn_output_weights += attn_mask

        if key_padding_mask is not None:
            attn_output_weights = attn_output_weights.view(
                b, self.num_heads, target_len, source_len
            )

            attn_output_weights = attn_output_weights.masked_fill(
                key_padding_mask.unsqueeze(1).unsqueeze(2),
                float("-inf"),
            )
            attn_output_weights = attn_output_weights.view(
                b * self.num_heads, target_len, source_len
            )

        attn_output_weights_raw = softmax(attn_output_weights, dim=-1)

        attn_output_weights = self.dropout(attn_output_weights_raw)

        attn_output = torch.bmm(attn_output_weights, v)
        attn_output = attn_output.transpose(0, 1).contiguous().view(target_len, b, c)
        attn_output = self.out_proj(attn_output)

        if output_weights:
            attn_output_weights_raw = attn_output_weights_raw.view(
                b, self.num_heads, target_len, source_len
            )
            return attn_output, attn_output_weights_raw.sum(dim=1) / self.num_heads
        return attn_output

    def init_weights(self):
        xavier_uniform_(self.in_proj_q.weight)
        xavier_uniform_(self.in_proj_k.weight)
        if self.proj_value:
            xavier_uniform_(self.in_proj_v.weight)


class GlobalDecoderLayer(Module):
    """
    Transformer Decoder Layer
    """

    def __init__(self, params):
        super(GlobalDecoderLayer, self).__init__()
        self.self_att = CustomMultiHeadAttention(
            embed_dim=params["enc_dim"],
            num_heads=params["dec_num_heads"],
            proj_value=True,
            dropout=params["dec_att_dropout"],
        )

        self.norm1 = LayerNorm(params["enc_dim"])
        self.att = CustomMultiHeadAttention(
            embed_dim=params["enc_dim"],
            num_heads=params["dec_num_heads"],
            proj_value=True,
            dropout=params["dec_att_dropout"],
        )

        self.linear1 = Linear(params["enc_dim"], params["dec_dim_feedforward"])
        self.linear2 = Linear(params["dec_dim_feedforward"], params["enc_dim"])

        self.dropout = Dropout(params["dec_res_dropout"])

        self.norm2 = LayerNorm(params["enc_dim"])
        self.norm3 = LayerNorm(params["enc_dim"])

    def forward(
        self,
        tgt,
        memory_key,
        memory_value=None,
        tgt_mask=None,
        memory_mask=None,
        tgt_key_padding_mask=None,
        memory_key_padding_mask=None,
        predict_last_n_only=None,
    ):
        if memory_value is None:
            memory_value = memory_key

        self_att_query = tgt[-predict_last_n_only:] if predict_last_n_only else tgt

        tgt2, weights_self = self.self_att(
            self_att_query,
            tgt,
            tgt,
            attn_mask=tgt_mask,
            key_padding_mask=tgt_key_padding_mask,
            output_weights=True,
        )
        tgt = self_att_query + self.dropout(tgt2)
        tgt = self.norm1(tgt)
        att_query = tgt

        tgt2, weights = self.att(
            att_query,
            memory_key,
            memory_value,
            attn_mask=memory_mask,
            key_padding_mask=memory_key_padding_mask,
            output_weights=True,
        )

        tgt = att_query + self.dropout(tgt2)
        tgt = self.norm2(tgt)
        tgt2 = self.linear2(self.dropout(relu(self.linear1(tgt))))
        tgt = tgt + self.dropout(tgt2)
        tgt = self.norm3(tgt)
        return tgt, weights, weights_self


class GlobalAttDecoder(Module):
    """
    Stack of transformer decoder layers
    """

    def __init__(self, params):
        super(GlobalAttDecoder, self).__init__()

        self.decoder_layers = ModuleList(
            [GlobalDecoderLayer(params) for _ in range(params["dec_num_layers"])]
        )

    def forward(
        self,
        tgt,
        memory_key,
        memory_value,
        tgt_mask,
        memory_mask,
        tgt_key_padding_mask,
        memory_key_padding_mask,
        use_cache=False,
        cache=None,
        predict_last_n_only=False,
        keep_all_weights=False,
    ):
        output = tgt
        cache_t = list()
        all_weights = {"self": list(), "mix": list()}

        for i, dec_layer in enumerate(self.decoder_layers):
            output, weights, weights_self = dec_layer(
                output,
                memory_key=memory_key,
                memory_value=memory_value,
                tgt_mask=tgt_mask,
                memory_mask=memory_mask,
                tgt_key_padding_mask=tgt_key_padding_mask,
                memory_key_padding_mask=memory_key_padding_mask,
                predict_last_n_only=predict_last_n_only,
            )
            if use_cache:
                cache_t.append(output)
                if cache is not None:
                    output = torch.cat([cache[i], output], dim=0)
            if keep_all_weights:
                all_weights["self"].append(weights_self)
                all_weights["mix"].append(weights)
        if use_cache:
            cache = (
                torch.cat([cache, torch.stack(cache_t, dim=0)], dim=1)
                if cache is not None
                else torch.stack(cache_t, dim=0)
            )

        if predict_last_n_only:
            output = output[-predict_last_n_only:]

        if keep_all_weights:
            return output, all_weights, cache

        return output, weights, cache


class FeaturesUpdater(Module):
    """
    Module that handle 2D positional encoding
    """

    def __init__(self, params):
        super(FeaturesUpdater, self).__init__()
        self.pe_2d = PositionalEncoding2D(
            params["enc_dim"], params["h_max"], params["w_max"], params["device"]
        )

    def get_pos_features(self, features):
        return self.pe_2d(features)


class GlobalHTADecoder(Module):
    """
    DAN decoder module
    """

    def __init__(self, params):
        super(GlobalHTADecoder, self).__init__()
        self.dropout = Dropout(params["dec_pred_dropout"])
        self.dec_att_win = (
            params["attention_win"] if params["attention_win"] is not None else 1
        )

        self.features_updater = FeaturesUpdater(params)
        self.att_decoder = GlobalAttDecoder(params)

        self.emb = Embedding(
            num_embeddings=params["vocab_size"] + 3, embedding_dim=params["enc_dim"]
        )
        self.pe_1d = PositionalEncoding1D(
            params["enc_dim"], params["l_max"], params["device"]
        )

        vocab_size = params["vocab_size"] + 1
        self.end_conv = Conv1d(params["enc_dim"], vocab_size, kernel_size=1)

    def forward(
        self,
        features_1d,
        tokens,
        reduced_size,
        token_len,
        features_size,
        start=0,
        hidden_predict=None,
        cache=None,
        num_pred=None,
        keep_all_weights=False,
    ):
        device = features_1d.device

        # Token to Embedding
        pos_tokens = self.emb(tokens).permute(0, 2, 1)

        # Add 1D Positional Encoding
        pos_tokens = self.pe_1d(pos_tokens, start=start).permute(2, 0, 1)

        if num_pred is None:
            num_pred = tokens.size(1)

        # Use cache values to avoid useless computation at eval time
        if self.dec_att_win > 1 and cache is not None:
            cache = cache[:, -self.dec_att_win + 1 :]
        else:
            cache = None
        num_tokens_to_keep = min(
            [num_pred + self.dec_att_win - 1, pos_tokens.size(0), token_len[0]]
        )
        pos_tokens = pos_tokens[-num_tokens_to_keep:]

        # Generate dynamic masks
        target_mask = self.generate_target_mask(
            tokens.size(1), device
        )  # Use only already predicted tokens (causal)
        memory_mask = None  # Use all feature position

        # Generate static masks
        key_target_mask = self.generate_token_mask(
            token_len, tokens.size(), device
        )  # Use all token except padding
        key_memory_mask = self.generate_enc_mask(
            reduced_size, features_size, device
        )  # Use all feature position except padding

        target_mask = target_mask[-num_pred:, -num_tokens_to_keep:]
        key_target_mask = key_target_mask[:, -num_tokens_to_keep:]

        output, weights, cache = self.att_decoder(
            pos_tokens,
            memory_key=features_1d,
            memory_value=features_1d,
            tgt_mask=target_mask,
            memory_mask=memory_mask,
            tgt_key_padding_mask=key_target_mask,
            memory_key_padding_mask=key_memory_mask,
            use_cache=True,
            cache=cache,
            predict_last_n_only=num_pred,
            keep_all_weights=keep_all_weights,
        )

        dp_output = self.dropout(relu(output))
        preds = self.end_conv(dp_output.permute(1, 2, 0))

        if not keep_all_weights:
            weights = torch.sum(weights, dim=1, keepdim=True).reshape(
                -1, 1, features_size[2], features_size[3]
            )
        return output, preds, hidden_predict, cache, weights

    def generate_enc_mask(self, batch_reduced_size, total_size, device):
        """
        Generate mask for encoded features
        """
        batch_size, _, h_max, w_max = total_size
        mask = torch.ones((batch_size, h_max, w_max), dtype=torch.bool, device=device)
        for i, (h, w) in enumerate(batch_reduced_size):
            mask[i, :h, :w] = False
        return torch.flatten(mask, start_dim=1, end_dim=2)

    def generate_token_mask(self, token_len, total_size, device):
        """
        Generate mask for tokens per sample
        """
        batch_size, len_max = total_size
        mask = torch.zeros((batch_size, len_max), dtype=torch.bool, device=device)
        for i, len_ in enumerate(token_len):
            mask[i, :len_] = False
        return mask

    def generate_target_mask(self, target_len, device):
        """
        Generate mask for tokens per time step (teacher forcing)
        """
        if self.dec_att_win == 1:
            return torch.triu(
                torch.ones((target_len, target_len), dtype=torch.bool, device=device),
                diagonal=1,
            )
        else:
            return torch.logical_not(
                torch.logical_and(
                    torch.tril(
                        torch.ones(
                            (target_len, target_len), dtype=torch.bool, device=device
                        ),
                        diagonal=0,
                    ),
                    torch.triu(
                        torch.ones(
                            (target_len, target_len), dtype=torch.bool, device=device
                        ),
                        diagonal=-self.dec_att_win + 1,
                    ),
                )
            )


class CTCLanguageDecoder:
    """
    Initialize a CTC decoder with n-gram language modeling.
    :param language_model_path: Path to a KenLM or ARPA language model.
    :param lexicon_path: Path to a lexicon file containing the possible words and corresponding spellings.
            Each line consists of a word and its space separated spelling. If `None`, uses lexicon-free decoding.
    :param tokens_path: Path to a file containing valid tokens. If using a file, the expected
            format is for tokens mapping to the same index to be on the same line.
    :param language_model_weight: Weight of the language model.
    :param temperature: Temperature for model calibreation.
    """

    def __init__(
        self,
        language_model_path: str,
        lexicon_path: str,
        tokens_path: str,
        language_model_weight: float = 1.0,
        temperature: float = 1.0,
    ):
        self.mapping = LMTokenMapping()
        self.language_model_weight = language_model_weight
        self.temperature = temperature
        self.tokens_to_index = {
            token: i for i, token in enumerate(read_txt(tokens_path).split("\n"))
        }
        self.index_to_token = {i: token for token, i in self.tokens_to_index.items()}
        self.blank_token_id = self.tokens_to_index[self.mapping.ctc.encoded]

        # Torchaudio's decoder
        # https://pytorch.org/audio/master/generated/torchaudio.models.decoder.ctc_decoder.html
        self.decoder = ctc_decoder(
            lm=language_model_path,
            lexicon=lexicon_path,
            tokens=tokens_path,
            lm_weight=self.language_model_weight,
            blank_token=self.mapping.ctc.encoded,
            sil_token=self.mapping.space.encoded,
            unk_word="⁇",
            nbest=1,
        )
        # No GPU support
        self.device = torch.device("cpu")

    def add_ctc_frames(
        self, batch_features: torch.FloatTensor, batch_frames: torch.LongTensor
    ) -> tuple[torch.FloatTensor, torch.LongTensor]:
        """
        Add CTC frames between each characters to avoid duplicate removal.
        """
        high_prob = batch_features.max()
        low_prob = batch_features.min()
        batch_size, n_frames, n_tokens = batch_features.shape
        # Reset probabilities for the CTC token
        batch_features[:, :, -1] = (
            torch.ones(
                (batch_size, n_frames),
                dtype=torch.float32,
                device=batch_features.device,
            )
            * low_prob
        )

        # Create a frame with high probability CTC token
        ctc_probs = (
            torch.ones(
                (batch_size, 1, n_tokens),
                dtype=torch.float32,
                device=batch_features.device,
            )
            * low_prob
        )
        ctc_probs[:, :, self.blank_token_id] = high_prob
        ctc_probs = ctc_probs

        # Insert the CTC frame between regular frames
        for fn in range(batch_frames.max() - 1):
            batch_features = torch.cat(
                [
                    batch_features[:, : 2 * fn + 1, :],
                    ctc_probs,
                    batch_features[:, 2 * fn + 1 :, :],
                ],
                dim=1,
            )

        # Update the number of frames
        batch_frames = 2 * batch_frames - 1
        return batch_features, batch_frames

    def post_process(
        self, hypotheses: List[CTCHypothesis], batch_sizes: torch.LongTensor
    ) -> Dict[str, List[str | float]]:
        """
        Post-process hypotheses to output JSON. Exports only the best hypothesis for each image.
        :param hypotheses: List of hypotheses returned by the decoder.
        :param batch_sizes: Prediction length of size batch_size.
        :return: A dictionary containing the hypotheses and their confidences.
        """
        out = {}
        # Replace <space> by an actual space and format string
        out["text"] = [
            "".join(
                [
                    self.mapping.display[self.index_to_token[token]]
                    if self.index_to_token[token] in self.mapping.display
                    else self.index_to_token[token]
                    for token in hypothesis[0].tokens.tolist()
                ]
            ).strip()
            for hypothesis in hypotheses
        ]
        # Normalize confidence score
        out["confidence"] = [
            np.around(
                np.exp(
                    hypothesis[0].score
                    / ((self.language_model_weight + 1) * length.item())
                ),
                2,
            )
            for hypothesis, length in zip(hypotheses, batch_sizes)
        ]
        return out

    def __call__(
        self, batch_features: torch.FloatTensor, batch_frames: torch.LongTensor
    ) -> Dict[str, List[str | float]]:
        """
        Decode a feature vector using n-gram language modelling.
        :param batch_features: Feature vector of size (batch_size, n_tokens, n_frames).
        :param batch_frames: Prediction length of size batch_size.
        :return: A dictionary containing the hypotheses and their confidences.
        """
        # Reshape from (batch_size, n_tokens, n_frames) to (batch_size, n_frames, n_tokens)
        batch_features = batch_features.permute((0, 2, 1))

        # Insert CTC frames to avoid getting rid of duplicates
        # Make sure that the CTC token has low probs for other frames
        batch_features, batch_frames = self.add_ctc_frames(batch_features, batch_frames)

        # Apply log softmax
        batch_features = torch.nn.functional.log_softmax(
            batch_features / self.temperature, dim=-1
        )

        # No GPU support for torchaudio's ctc_decoder
        batch_features = batch_features.to(self.device)
        batch_frames = batch_frames.to(self.device)

        # Decode
        hypotheses = self.decoder(batch_features, batch_frames)
        return self.post_process(hypotheses, batch_frames)
