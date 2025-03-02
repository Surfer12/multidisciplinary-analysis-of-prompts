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

"""Llama 3.2 Transformer Vision Language Model cross attention decoder."""

from __future__ import annotations

from dataclasses import dataclass

from max.dtype import DType
from max.graph import TensorValue, Weight, ops
from max.pipelines.kv_cache import ContinuousBatchingKVCacheCollection, KVCacheParams
from nn import MLP, RMSNorm
from nn.kernels import flash_attention_ragged_with_causal_mask, matmul_kv_cache_ragged
from nn.layer import Layer
from nn.linear import Linear


@dataclass
class CrossSdpaAttention(Layer):
    n_heads: int
    """The number of attention heads."""

    kv_params: KVCacheParams
    """KV Cache Params, including the number of kv heads, the head dim, and data type."""

    layer_idx: int
    """The layer number associated with this Attention block."""

    q_proj: Linear
    """A linear layer for the query projection."""

    wk: Weight
    """The k weight vector. Combines with wv to form a Linear."""

    wv: Weight
    """The v weight vector. Combines with wk to form a Linear."""

    o_proj: Linear
    """A linear layer for the output projection."""

    q_norm: RMSNorm
    """Layer normalization."""

    k_norm: RMSNorm
    """Layer normalization."""

    def __call__(
        self,
        hidden_states: TensorValue,
        hidden_input_row_offsets: TensorValue,
        cross_attention_states: TensorValue,
        cross_input_row_offsets: TensorValue,
        kv_collection: ContinuousBatchingKVCacheCollection,
    ) -> TensorValue:
        """Computes attention on hidden (query) and cross (key and value).

        Returns:
            Attended hidden activation.
        """
        # Get the combined sequence length: sum(seq_len for seq_len in batch).
        total_seq_len = hidden_states.shape[0]

        wkv = ops.concat((self.wk, self.wv), axis=0)

        query_states = self.q_proj(hidden_states)
        query_states = query_states.reshape(
            [
                -1,
                self.n_heads,
                self.kv_params.head_dim,
            ]
        )
        query_states = self.q_norm(query_states)

        matmul_kv_cache_ragged(
            kv_params=self.kv_params,
            # Here, hidden_states correspond to cross_attention_states.
            hidden_states=cross_attention_states,
            layer_idx=self.layer_idx,
            input_row_offsets=cross_input_row_offsets,
            weight=wkv,
            kv_collection=kv_collection,
        )

        # Calculate Flash Attention.
        attn_out = flash_attention_ragged_with_causal_mask(
            self.kv_params,
            input=query_states,
            kv_collection=kv_collection,
            layer_idx=ops.constant(self.layer_idx, DType.uint32),
            input_row_offsets=hidden_input_row_offsets,
        )

        attn_out = ops.reshape(attn_out, shape=[total_seq_len, -1])

        return self.o_proj(attn_out)


@dataclass
class CrossAttentionDecoderLayer(Layer):
    """Cross-attention transformer block with tanh-gated attention and feedforward."""

    cross_attn: CrossSdpaAttention
    input_layernorm: RMSNorm
    cross_attn_attn_gate: Weight
    mlp: MLP
    post_attention_layernorm: RMSNorm
    cross_attn_mlp_gate: Weight

    def __call__(
        self,
        hidden_states: TensorValue,
        hidden_input_row_offsets: TensorValue,
        cross_attention_states: TensorValue,
        cross_input_row_offsets: TensorValue,
        kv_collection: ContinuousBatchingKVCacheCollection,
    ) -> TensorValue:
        residual = hidden_states
        hidden_states = self.input_layernorm(hidden_states)
        assert (
            len(cross_attention_states.shape) == 2
        ), "cross_attn is expecting a ragged tensor"

        hidden_states = self.cross_attn(
            hidden_states,
            hidden_input_row_offsets,
            cross_attention_states,
            cross_input_row_offsets,
            kv_collection,
        )
        hidden_states = residual + ops.tanh(self.cross_attn_attn_gate) * hidden_states

        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = self.mlp(hidden_states)
        return residual + ops.tanh(self.cross_attn_mlp_gate) * hidden_states
