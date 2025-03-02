# ===----------------------------------------------------------------------=== #
# Copyright (c) 2024, Modular Inc. All rights reserved.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions:
# https://llvm.org/LICENSE.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===----------------------------------------------------------------------=== #

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from functools import cached_property
from os import PathLike
from pathlib import Path

import torch
from max.dtype import DType
from max.graph.weights import SafetensorWeights, WeightsConverter
from max.graph.weights._torch_dtype_map import (
    modular_to_torch_type,
    torch_to_modular_type,
)
from transformers import LlamaConfig

# Map from GGUF tensor names to Safetensor names.
# https://github.com/huggingface/transformers/blob/7bbc62474391aff64f63fcc064c975752d1fa4de/src/transformers/integrations/ggml.py#L36
LLAMA_GGUF_TENSOR_MAPPING = {
    "token_embd": "model.embed_tokens",
    "blk": "model.layers",
    "ffn_up": "mlp.up_proj",
    "ffn_down": "mlp.down_proj",
    "ffn_gate": "mlp.gate_proj",
    "ffn_norm": "post_attention_layernorm",
    "attn_norm": "input_layernorm",
    "attn_q": "self_attn.q_proj",
    "attn_v": "self_attn.v_proj",
    "attn_k": "self_attn.k_proj",
    "attn_output": "self_attn.o_proj",
    "output.weight": "lm_head.weight",
    "output_norm": "model.norm",
}


class LlamaSafetensorWeights(SafetensorWeights, WeightsConverter):
    """Loads Safetensor weights with GGUF names.

    Does the following when loading weights:
    (1) converts Safetensor weight names to GGUF names. For example, the
    GGUF weight "blk.{i}.attn_q.weight" is instead saved as
    "model.layers.{i}.self_attn.q_proj.weight" in Safetensor.
    (2) Computes the rope_freqs.weight using the HuggingFace config
    (3) Transposes the q_proj and k_proj weights.

    """

    def __init__(
        self,
        filepaths: Sequence[PathLike],
        gguf_name_map: Mapping[str, str],
        huggingface_config: LlamaConfig,
        has_rope_scaling: bool,
        rope_freqs_tensor: torch.Tensor | None,
        **kwargs,
    ):
        super().__init__(filepaths, **kwargs)
        self._gguf_name_map = gguf_name_map
        self._huggingface_config = huggingface_config
        self._has_rope_scaling = has_rope_scaling
        self._rope_freqs_tensor = rope_freqs_tensor

    @staticmethod
    def load_weights(weight_path: list[Path], **kwargs):
        config = kwargs["config"]

        huggingface_config = config.huggingface_config
        has_rope_scaling = False
        rope_freqs_tensor = None
        if rope_scaling := huggingface_config.rope_scaling:
            if rope_scaling.get("rope_type", "").lower() == "llama3":
                has_rope_scaling = True
                rope_freqs_tensor = _compute_rope_scaling(
                    rope_scaling, huggingface_config
                )

        return LlamaSafetensorWeights(
            weight_path,
            gguf_name_map=LLAMA_GGUF_TENSOR_MAPPING,
            huggingface_config=config.huggingface_config,
            has_rope_scaling=has_rope_scaling,
            rope_freqs_tensor=rope_freqs_tensor,
        )

    def items(self):
        # This is defined in SafetensorWeights. Currently there's no reason to
        # use this LlamaSafetensorWeights, so it is unimplemented.
        raise NotImplementedError

    @cached_property
    def name(self) -> str:
        """The current weight name or prefix."""
        name = self._prefix
        if self._gguf_name_map:
            # Note that the following replacement only works for models like
            # Llama or Mistral which do not include `{bid}` (block ID) in the
            # name map.
            for before, after in self._gguf_name_map.items():
                name = name.replace(before, after)
        return name

    def __getattr__(self, attr) -> LlamaSafetensorWeights:
        if self._prefix:
            full_path = f"{self._prefix}.{attr}"
        else:
            full_path = str(attr)
        return LlamaSafetensorWeights(
            self._filepaths,
            self._gguf_name_map,
            huggingface_config=self._huggingface_config,
            has_rope_scaling=self._has_rope_scaling,
            rope_freqs_tensor=self._rope_freqs_tensor,
            tensors=self._tensors,
            tensors_to_file_idx=self._tensors_to_file_idx,
            prefix=full_path,
            allocated=self._allocated,
            _st_weight_map=self._st_weight_map,
        )

    def exists(self) -> bool:
        return self.name in self._tensors_to_file_idx or (
            self._has_rope_scaling and self.name == "rope_freqs.weight"
        )

    def _load_tensor(self, dtype: DType | None = None):
        if self._has_rope_scaling and self.name == "rope_freqs.weight":
            tensor = self._rope_freqs_tensor
            assert isinstance(tensor, torch.Tensor)
            if dtype is not None and torch_to_modular_type(tensor.dtype) != dtype:
                tensor = tensor.to(modular_to_torch_type(dtype))
            return tensor
        tensor = super()._load_tensor(dtype)

        if self.name.endswith(("q_proj.weight", "q_proj.bias")):
            n_head = self._huggingface_config.num_attention_heads
            tensor = _permute_weights(tensor, n_head, n_head)
        elif self.name.endswith(("k_proj.weight", "k_proj.bias")):
            n_head = self._huggingface_config.num_attention_heads
            n_kv_head = self._huggingface_config.num_key_value_heads
            tensor = _permute_weights(tensor, n_head, n_kv_head)

        return tensor


def _compute_rope_scaling(rope_scaling, huggingface_config: LlamaConfig):
    # From llama.cpp's HF to GGUF conversion script:
    # https://github.com/ggerganov/llama.cpp/blob/40c6d79fb52f995f47507fedfeaae2ac05d9b35c/convert_hf_to_gguf.py#L1627-L1654
    base = huggingface_config.rope_theta
    dim = huggingface_config.head_dim
    freqs = 1.0 / (base ** (torch.arange(0, dim, 2, dtype=torch.float32) / dim))

    factor = rope_scaling.get("factor", 8.0)
    low_freq_factor = rope_scaling.get("low_freq_factor", 1.0)
    high_freq_factor = rope_scaling.get("high_freq_factor", 4.0)
    old_context_len = rope_scaling.get("original_max_position_embeddings", 8192)

    low_freq_wavelen = old_context_len / low_freq_factor
    high_freq_wavelen = old_context_len / high_freq_factor
    assert low_freq_wavelen != high_freq_wavelen

    rope_factors = []
    for freq in freqs:
        wavelen = 2 * math.pi / freq
        if wavelen < high_freq_wavelen:
            rope_factors.append(1)
        elif wavelen > low_freq_wavelen:
            rope_factors.append(factor)
        else:
            smooth = (old_context_len / wavelen - low_freq_factor) / (
                high_freq_factor - low_freq_factor
            )
            rope_factors.append(1 / ((1 - smooth) / factor + smooth))
    return torch.tensor(rope_factors, dtype=torch.float32)


def _permute_weights(weights: torch.Tensor, n_head: int, n_head_kv: int | None):
    # From llama.cpp's HF to GGUF conversion script:
    # https://github.com/ggerganov/llama.cpp/blob/40c6d79fb52f995f47507fedfeaae2ac05d9b35c/convert_hf_to_gguf.py#L1571C1-L1578C41
    if n_head_kv is not None and n_head != n_head_kv:
        n_head = n_head_kv
    return (
        weights.reshape(n_head, 2, weights.shape[0] // n_head // 2, *weights.shape[1:])
        .swapaxes(1, 2)
        .reshape(weights.shape)
    )
