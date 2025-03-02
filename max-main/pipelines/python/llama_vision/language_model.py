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

"""Llama 3.2 Transformer Vision Language Model."""

from __future__ import annotations

from dataclasses import dataclass

from max.dtype import DType
from max.graph import TensorValue, ops
from max.graph.weights import Weights
from max.pipelines.kv_cache import (
    FetchContinuousBatchingKVCacheCollection,
    KVCacheParams,
)
from nn import (
    MLP,
    AttentionWithRopeQKV,
    Embedding,
    Linear,
    OptimizedRotaryEmbedding,
    RMSNorm,
    TransformerBlock,
)
from nn.layer import Layer

from .cross_attention_decoder import CrossAttentionDecoderLayer, CrossSdpaAttention


@dataclass
class TextModel(Layer):
    """
    The Llama text model which consists of transformer with self and cross attention layers.
    """

    dtype: DType
    kv_params: KVCacheParams
    embed_tokens: Embedding
    layers: list[CrossAttentionDecoderLayer | TransformerBlock]
    norm: RMSNorm
    cross_attention_layers: list[int]
    rotary_emb: OptimizedRotaryEmbedding

    # input_ids: shape=[1, 1], dtype=torch.int64
    # attention_mask: shape=[1, 22], dtype=torch.int64
    # position_ids: shape=[1, 1], dtype=torch.int64
    # cross_attention_states: value=None
    # cross_attention_mask: shape=[1, 1, 1, 4100], dtype=torch.bfloat16
    # full_text_row_masked_out_mask: shape=[1, 1, 1, 1], dtype=torch.bfloat16
    # past_key_values: value=DynamicCache()
    # inputs_embeds: value=None
    # use_cache: value=True
    # output_attentions: value=False
    # output_hidden_states: value=False
    # return_dict: value=True

    def __call__(
        self,
        kv_cache_inputs: tuple[TensorValue, ...],
        input_ids: TensorValue,
        hidden_input_row_offsets: TensorValue,
        cross_attention_states: TensorValue,
        cross_input_row_offsets: TensorValue,
    ) -> TensorValue:
        inputs_embeds = self.embed_tokens(input_ids)

        hidden_states = ops.cast(inputs_embeds, self.dtype)

        # TODO: This hacky reshape is needed to go from rank 3 -> 2 (ragged tensor).
        hidden_size = hidden_states.shape[-1]
        hidden_states = hidden_states.reshape((-1, hidden_size))

        for idx, decoder_layer in enumerate(self.layers):
            # For text-only path we should skip cross attention layers.
            # Let's check if the layer is cross attention layer and if we have
            # cross attention states.
            if idx in self.cross_attention_layers and cross_attention_states is None:
                continue

            kv_collection_constructor = FetchContinuousBatchingKVCacheCollection(
                self.kv_params
            )
            kv_collection = kv_collection_constructor(*kv_cache_inputs)

            if isinstance(decoder_layer, CrossAttentionDecoderLayer):
                hidden_states = decoder_layer(
                    hidden_states,
                    hidden_input_row_offsets,
                    cross_attention_states,
                    cross_input_row_offsets,
                    kv_collection,
                )
            else:
                hidden_states = decoder_layer(
                    hidden_states,
                    kv_collection,
                    input_row_offsets=hidden_input_row_offsets,
                )

        return self.norm(hidden_states)


@dataclass
class CausalLanguageModel(Layer):
    """The Llama Vision Text Model with a language modeling head on top."""

    dtype: DType
    kv_params: KVCacheParams
    model: TextModel
    lm_head: Linear

    # input_ids: shape=[1, 14], dtype=torch.int64
    # attention_mask: shape=[1, 14], dtype=torch.int64
    # position_ids: shape=[1, 14], dtype=torch.int64
    # cross_attention_states: shape=[4, 1025, 4096], dtype=torch.bfloat16
    # cross_attention_mask: shape=[1, 1, 14, 4100], dtype=torch.bfloat16
    # full_text_row_masked_out_mask: shape=[1, 1, 14, 1], dtype=torch.bfloat16
    # past_key_values: value=DynamicCache()
    # inputs_embeds: value=None
    # labels: value=None
    # use_cache: value=True
    # output_attentions: value=False
    # output_hidden_states: value=False
    # return_dict: value=True
    # cache_position: shape=[14], dtype=torch.int64
    # num_logits_to_keep: value=1

    def __call__(
        self,
        kv_cache_inputs: tuple[TensorValue, ...],
        input_ids: TensorValue,
        hidden_input_row_offsets: TensorValue,
        cross_attention_states: TensorValue,
        cross_input_row_offsets: TensorValue,
    ) -> TensorValue:
        last_hidden_state = self.model(
            kv_cache_inputs,
            input_ids,
            hidden_input_row_offsets,
            cross_attention_states,
            cross_input_row_offsets,
        )

        # For ragged tensors gather the last tokens from packed dim 0.
        last_token_indices = hidden_input_row_offsets[1:] - 1
        last_token_logits = ops.gather(last_hidden_state, last_token_indices, axis=0)
        return ops.cast(self.lm_head(last_token_logits), self.dtype)  # logits


def cross_attention_decoder_layer(
    dtype: DType,
    num_attention_heads: int,
    hidden_size: int,
    num_key_value_heads: int,
    rms_norm_eps: float,
    kv_params: KVCacheParams,
    intermediate_size: int,
    weights: Weights,
    layer_idx: int,
) -> CrossAttentionDecoderLayer:
    head_dim = hidden_size // num_attention_heads
    sdpa_attn = CrossSdpaAttention(
        n_heads=num_attention_heads,
        kv_params=kv_params,
        layer_idx=layer_idx,
        q_proj=Linear(
            weights.cross_attn.q_proj.weight.allocate(
                dtype,
                [
                    num_attention_heads * head_dim,
                    hidden_size,
                ],
            ),
            bias=None,
        ),
        wk=weights.cross_attn.k_proj.weight.allocate(
            dtype,
            [
                num_key_value_heads * head_dim,
                hidden_size,
            ],
        ),
        wv=weights.cross_attn.v_proj.weight.allocate(
            dtype,
            [
                num_key_value_heads * head_dim,
                hidden_size,
            ],
        ),
        o_proj=Linear(
            weight=weights.cross_attn.o_proj.weight.allocate(
                dtype,
                [
                    hidden_size,
                    num_attention_heads * head_dim,
                ],
            ),
            bias=None,
        ),
        q_norm=RMSNorm(
            weight=weights.cross_attn.q_norm.weight.allocate(
                dtype,
                [head_dim],
            ),
            eps=rms_norm_eps,
        ),
        k_norm=RMSNorm(
            weight=weights.cross_attn.k_norm.weight.allocate(
                dtype,
                [head_dim],
            ),
            eps=rms_norm_eps,
        ),
    )
    return CrossAttentionDecoderLayer(
        cross_attn=sdpa_attn,
        input_layernorm=RMSNorm(
            weight=weights.input_layernorm.weight.allocate(
                dtype,
                [hidden_size],
            ),
            eps=rms_norm_eps,
        ),
        cross_attn_attn_gate=weights.cross_attn_attn_gate.allocate(
            dtype,
            [1],
        ),
        mlp=MLP(
            gate_proj=Linear(
                weight=weights.mlp.gate_proj.weight.allocate(
                    dtype,
                    [
                        intermediate_size,
                        hidden_size,
                    ],
                ),
                bias=None,
            ),
            down_proj=Linear(
                weight=weights.mlp.down_proj.weight.allocate(
                    dtype,
                    [
                        hidden_size,
                        intermediate_size,
                    ],
                ),
                bias=None,
            ),
            up_proj=Linear(
                weight=weights.mlp.up_proj.weight.allocate(
                    dtype,
                    [
                        intermediate_size,
                        hidden_size,
                    ],
                ),
                bias=None,
            ),
        ),
        post_attention_layernorm=RMSNorm(
            weight=weights.post_attention_layernorm.weight.allocate(
                dtype,
                [hidden_size],
            ),
            eps=rms_norm_eps,
        ),
        cross_attn_mlp_gate=weights.cross_attn_mlp_gate.allocate(
            dtype,
            [1],
        ),
    )


def self_attention_decoder_layer(
    dtype: DType,
    num_attention_heads: int,
    hidden_size: int,
    num_key_value_heads: int,
    intermediate_size: int,
    rms_norm_eps: float,
    kv_params: KVCacheParams,
    weights: Weights,
    layer_idx: int,
    rotary_embedding: OptimizedRotaryEmbedding,
) -> TransformerBlock:
    head_dim = hidden_size // num_attention_heads

    wq = weights.self_attn.q_proj.weight.allocate(
        dtype, shape=[num_attention_heads * head_dim, hidden_size]
    )
    wk = weights.self_attn.k_proj.weight.allocate(
        dtype, shape=[num_key_value_heads * head_dim, hidden_size]
    )
    wv = weights.self_attn.v_proj.weight.allocate(
        dtype, shape=[num_key_value_heads * head_dim, hidden_size]
    )
    o_proj = Linear(
        weight=weights.self_attn.o_proj.weight.allocate(
            dtype,
            shape=[hidden_size, num_attention_heads * head_dim],
        )
    )

    attention = AttentionWithRopeQKV(
        n_heads=num_attention_heads,
        kv_params=kv_params,
        layer_idx=layer_idx,
        wq=wq,
        wk=wk,
        wv=wv,
        wo=o_proj,
        rope=rotary_embedding,
    )

    return TransformerBlock(
        attention=attention,
        mlp=MLP(
            gate_proj=Linear(
                weight=weights.mlp.gate_proj.weight.allocate(
                    dtype,
                    [intermediate_size, hidden_size],
                ),
                bias=None,
            ),
            down_proj=Linear(
                weight=weights.mlp.down_proj.weight.allocate(
                    dtype,
                    [hidden_size, intermediate_size],
                ),
                bias=None,
            ),
            up_proj=Linear(
                weight=weights.mlp.up_proj.weight.allocate(
                    dtype,
                    [intermediate_size, hidden_size],
                ),
                bias=None,
            ),
        ),
        attention_norm=RMSNorm(
            weight=weights.input_layernorm.weight.allocate(
                dtype,
                [hidden_size],
            ),
            eps=rms_norm_eps,
        ),
        mlp_norm=RMSNorm(
            weight=weights.post_attention_layernorm.weight.allocate(
                dtype, [hidden_size]
            ),
            eps=rms_norm_eps,
        ),
    )


def instantiate_language_model(
    dtype: DType,
    hidden_size: int,
    n_heads: int,
    rope_theta: int,
    max_seq_len: int,
    num_hidden_layers: int,
    cross_attention_layers: list[int],
    vocab_size: int,
    rms_norm_eps: float,
    num_key_value_heads: int,
    intermediate_size: int,
    kv_params: KVCacheParams,
    weights: Weights,
) -> CausalLanguageModel:
    layers: list[CrossAttentionDecoderLayer | TransformerBlock] = []

    # We don't really have a rotary embedding layer within the graph as it's largely
    # folded into the custom kernel, but leaving this here for now.
    rotary_embedding = OptimizedRotaryEmbedding(
        dim=hidden_size,
        n_heads=n_heads,
        theta=rope_theta,
        max_seq_len=max_seq_len,
        # TODO: Figure out how we want to pass this
        # rope_scaling=params.rope_scaling,
    )

    for layer_idx in range(
        num_hidden_layers,
    ):
        curr_layer_weight = weights.language_model.model.layers[layer_idx]

        if layer_idx in cross_attention_layers:
            layers.append(
                cross_attention_decoder_layer(
                    dtype=dtype,
                    num_attention_heads=n_heads,
                    hidden_size=hidden_size,
                    num_key_value_heads=num_key_value_heads,
                    rms_norm_eps=rms_norm_eps,
                    kv_params=kv_params,
                    intermediate_size=intermediate_size,
                    weights=curr_layer_weight,
                    layer_idx=layer_idx,
                )
            )
        else:
            layers.append(
                self_attention_decoder_layer(
                    dtype=dtype,
                    num_attention_heads=n_heads,
                    hidden_size=hidden_size,
                    num_key_value_heads=num_key_value_heads,
                    intermediate_size=intermediate_size,
                    rms_norm_eps=rms_norm_eps,
                    kv_params=kv_params,
                    weights=curr_layer_weight,
                    layer_idx=layer_idx,
                    rotary_embedding=rotary_embedding,
                )
            )

    text_model = TextModel(
        dtype=dtype,
        kv_params=kv_params,
        embed_tokens=Embedding(
            weights.language_model.model.embed_tokens.weight.allocate(
                dtype,
                [
                    # Upstream in the Huggingface llama reference, 8 is added to the vocab size.
                    vocab_size + 8,
                    hidden_size,
                ],
            ),
        ),
        norm=RMSNorm(
            weight=weights.language_model.model.norm.weight.allocate(
                dtype,
                [hidden_size],
            ),
            eps=rms_norm_eps,
        ),
        layers=layers,
        cross_attention_layers=cross_attention_layers,
        # TODO: Verify if these values passed are even correct.
        rotary_emb=rotary_embedding,
    )

    return CausalLanguageModel(
        dtype=dtype,
        kv_params=kv_params,
        model=text_model,
        lm_head=Linear(
            weights.language_model.lm_head.weight.allocate(
                dtype,
                [
                    vocab_size,
                    hidden_size,
                ],
            ),
            bias=None,
        ),
    )
