import os
import random
import re
from typing import Generator

import numpy as np

from cipher.plugins.speech.phonemizers import CUSTOM_PHONEMIZERS, BasePhonemizer


def _linear_overlap_add(frames: list[np.ndarray], stride: int) -> np.ndarray:
    if not len(frames):
        return np.array([])
    dtype = frames[0].dtype
    shape = frames[0].shape[:-1]

    total_size = 0
    for i, frame in enumerate(frames):
        frame_end = stride * i + frame.shape[-1]
        total_size = max(total_size, frame_end)

    sum_weight = np.zeros(total_size, dtype=dtype)
    out = np.zeros(*shape, total_size, dtype=dtype)

    offset: int = 0
    for frame in frames:
        frame_length = frame.shape[-1]
        t = np.linspace(0, 1, frame_length + 2, dtype=dtype)[1:-1]
        weight = np.abs(0.5 - (t - 0.5))

        out[..., offset : offset + frame_length] += weight * frame
        sum_weight[offset : offset + frame_length] += weight
        offset += stride
    assert sum_weight.min() > 0
    return out / sum_weight

class NeuTTSLite:
    def __init__(
        self,
        backbone_repo="neuphonic/neutts-nano-french-q4-gguf",
        codec_repo="neuphonic/neucodec-onnx-decoder",
        language="fr-fr",
    ):
        self.sample_rate = 24_000
        self.max_context = 2048
        self.hop_length = 480
        self.streaming_overlap_frames = 1
        self.streaming_frames_per_chunk = 25
        self.streaming_lookforward = 5
        self.streaming_lookback = 50
        self.streaming_stride_samples = self.streaming_frames_per_chunk * self.hop_length

        if language in CUSTOM_PHONEMIZERS:
            self.phonemizer = CUSTOM_PHONEMIZERS[language]
        else:
            self.phonemizer = BasePhonemizer(language_code=language)

        self._load_backbone(backbone_repo)
        self._load_codec(codec_repo)

    def _load_backbone(self, backbone_repo):
        import logging

        from llama_cpp import Llama

        seed = random.randint(0, 2**32)
        if os.path.isfile(backbone_repo):
            self.backbone = Llama(
                model_path=backbone_repo,
                verbose=False,
                n_ctx=self.max_context,
                seed=seed,
            )
        else:
            logging.info(f"Downloading backbone {backbone_repo}...")
            self.backbone = Llama.from_pretrained(
                repo_id=backbone_repo,
                filename="*.gguf",
                verbose=False,
                n_ctx=self.max_context,
                seed=seed,
            )

    def _load_codec(self, codec_repo):
        import logging

        import onnxruntime
        from huggingface_hub import hf_hub_download

        if os.path.isfile(codec_repo):
            model_path = codec_repo
        else:
            logging.info(f"Downloading codec {codec_repo}...")
            model_path = hf_hub_download(repo_id=codec_repo, filename="model.onnx")

        so = onnxruntime.SessionOptions()
        so.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = onnxruntime.InferenceSession(model_path, sess_options=so)

    def _to_phones(self, text: str) -> str:
        phones = self.phonemizer.phonemize([text])
        phones = phones[0].split()
        return " ".join(phones)

    def _decode(self, codes: str):
        speech_ids = [int(num) for num in re.findall(r"<\|speech_(\d+)\|>", codes)]
        if len(speech_ids) > 0:
            codes_arr = np.array(speech_ids, dtype=np.int32)[np.newaxis, np.newaxis, :]
            recon = self.session.run(None, {"codes": codes_arr})[0]
            return recon[0, 0, :]
        else:
            raise ValueError("No valid speech tokens found in the output.")

    def infer_stream(
        self, text: str, ref_codes: np.ndarray, ref_text: str
    ) -> Generator[np.ndarray, None, None]:
        ref_text = self._to_phones(ref_text)
        input_text = self._to_phones(text)

        codes_str = "".join([f"<|speech_{idx}|>" for idx in ref_codes.flatten()])
        prompt = (
            f"user: Convert the text to speech:<|TEXT_PROMPT_START|>{ref_text} {input_text}"
            f"<|TEXT_PROMPT_END|>\nassistant:<|SPEECH_GENERATION_START|>{codes_str}"
        )

        audio_cache: list[np.ndarray] = []
        token_cache: list[str] = [f"<|speech_{idx}|>" for idx in ref_codes.flatten()]
        n_decoded_samples: int = 0
        n_decoded_tokens: int = len(ref_codes.flatten())

        for item in self.backbone(
            prompt,
            max_tokens=self.max_context,
            temperature=1.0,
            top_k=50,
            stop=["<|SPEECH_GENERATION_END|>"],
            stream=True,
        ):
            output_str = item["choices"][0]["text"]
            token_cache.append(output_str)

            if (
                len(token_cache[n_decoded_tokens:])
                >= self.streaming_frames_per_chunk + self.streaming_lookforward
            ):
                tokens_start = max(
                    n_decoded_tokens - self.streaming_lookback - self.streaming_overlap_frames, 0
                )
                tokens_end = (
                    n_decoded_tokens
                    + self.streaming_frames_per_chunk
                    + self.streaming_lookforward
                    + self.streaming_overlap_frames
                )
                sample_start = (n_decoded_tokens - tokens_start) * self.hop_length
                sample_end = (
                    sample_start
                    + (self.streaming_frames_per_chunk + 2 * self.streaming_overlap_frames)
                    * self.hop_length
                )
                curr_codes = token_cache[tokens_start:tokens_end]
                try:
                    recon = self._decode("".join(curr_codes))
                    recon = recon[sample_start:sample_end]
                    audio_cache.append(recon)

                    processed_recon = _linear_overlap_add(
                        audio_cache, stride=self.streaming_stride_samples
                    )
                    new_samples_end = len(audio_cache) * self.streaming_stride_samples
                    processed_recon = processed_recon[n_decoded_samples:new_samples_end]
                    n_decoded_samples = new_samples_end
                    n_decoded_tokens += self.streaming_frames_per_chunk
                    yield processed_recon
                except ValueError:
                    pass

        remaining_tokens = len(token_cache) - n_decoded_tokens
        if len(token_cache) > n_decoded_tokens:
            tokens_start = max(
                len(token_cache)
                - (self.streaming_lookback + self.streaming_overlap_frames + remaining_tokens),
                0,
            )
            sample_start = (
                len(token_cache) - tokens_start - remaining_tokens - self.streaming_overlap_frames
            ) * self.hop_length
            curr_codes = token_cache[tokens_start:]
            try:
                recon = self._decode("".join(curr_codes))
                recon = recon[sample_start:]
                audio_cache.append(recon)

                processed_recon = _linear_overlap_add(audio_cache, stride=self.streaming_stride_samples)
                processed_recon = processed_recon[n_decoded_samples:]
                yield processed_recon
            except ValueError:
                pass
