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
"""An attention layer, using only native max graph operations, the naive cache, and ROPE."""

import math
from dataclasses import dataclass

from max.graph import BufferValue, TensorValue, TensorValueLike, ops
from max.pipelines.kv_cache import KVCacheParams, KVCacheStrategy

from ..layer import Layer
from ..linear import Linear
from ..rotary_embedding import RotaryEmbedding


@dataclass
class NaiveAttentionWithRope(Layer):
    n_heads: int
    kv_params: KVCacheParams
    dim: int

    wq: Linear
    wk: Linear
    wv: Linear
    wo: Linear

    rope: RotaryEmbedding

    def __post_init__(self) -> None:
        if self.kv_params.cache_strategy != KVCacheStrategy.NAIVE:
            raise ValueError(
                f"{self.kv_params.cache_strategy} cache strategy, not supported"
                " in Attention layer."
            )

    def repeat_kv(self, kv: TensorValue) -> TensorValue:
        """Repeats key/value tensors to match the number of query heads."""
        batch = kv.shape[0]
        kv = ops.reshape(
            kv,
            [batch, -1, self.kv_params.n_kv_heads, 1, self.kv_params.head_dim],
        )

        kv = ops.tile(kv, [1, 1, 1, self.n_heads // self.kv_params.n_kv_heads, 1])
        return ops.reshape(kv, [batch, -1, self.n_heads, self.kv_params.head_dim])

    def attention(
        self,
        xq: TensorValueLike,
        xk: TensorValueLike,
        xv: TensorValueLike,
        attn_mask: TensorValueLike,
        keys: TensorValueLike,
        values: TensorValueLike,
    ) -> TensorValue:
        # Broadcast the attention mask across heads.
        # Do so in the graph so that the broadcast can be fused downstream ops.
        batch, seq_len, post_seq_len = attn_mask.shape  # type: ignore
        attn_mask = attn_mask.reshape(  # type: ignore
            (batch, 1, seq_len, post_seq_len)  # type: ignore
        ).broadcast_to((batch, self.n_heads, seq_len, post_seq_len))

        keys = keys.transpose(0, 1)  # type: ignore
        values = values.transpose(0, 1)  # type: ignore

        keys = self.repeat_kv(keys)  # type: ignore
        values = self.repeat_kv(values)  # type: ignore

        xq = xq.transpose(1, 2)  # type: ignore
        keys = keys.transpose(1, 2)
        values = values.transpose(1, 2)

        scale = math.sqrt(1.0 / self.kv_params.head_dim)
        scores = xq @ ops.transpose(keys, 2, 3)
        # Note, the graph compiler currently requires the order of operands
        # to be `scores * scale` in order to pattern match the fused attention
        # operator.
        return ops.softmax(scores * scale + attn_mask) @ values

    def __call__(
        self,
        x: TensorValueLike,
        attention_mask: TensorValueLike,
        k_cache: BufferValue,
        v_cache: BufferValue,
        start_pos: TensorValue,
        layer_index: int,
    ) -> TensorValue:
        """Computes attention on x, reusing the KV cache.

        Args:
            x: Activations with shape (batch, seq_len, dim).
            k_cache: The full keys cache buffer with shape
                (max_seq_len, n_layers, max_batch, n_kv_heads, head_dim).
            v_cache: The full values cache buffer with shape
                (max_seq_len, n_layers, max_batch, n_kv_heads, head_dim).
            start_pos: Scalar of the current position in the kv_cache.

        Returns the result of multi-headed self attention on the input.
        """
        batch, seq_len = x.shape[0], x.shape[1]  # type: ignore
        # matmul weights
        xq = self.wq(x)  # type: ignore
        xk = self.wk(x)  # type: ignore
        xv = self.wv(x)  # type: ignore

        xq = ops.reshape(xq, [batch, seq_len, self.n_heads, self.kv_params.head_dim])

        xk = ops.reshape(
            xk,
            [
                batch,
                seq_len,
                self.kv_params.n_kv_heads,
                self.kv_params.head_dim,
            ],
        )
        xv = ops.reshape(
            xv,
            [
                batch,
                seq_len,
                self.kv_params.n_kv_heads,
                self.kv_params.head_dim,
            ],
        )

        xq = self.rope(xq, start_pos, seq_len)
        xk = self.rope(xk, start_pos, seq_len)

        # Write xk and xv back the to cache at start_pos.
        # The cache can have a larger max batch size than the current input.
        # We slice down to the active batch size.
        # cache[start_pos:start_pos+seq_len, layer_index, :batch] = ...
        seq_len_val = TensorValue(seq_len)
        slice_seq_len = (slice(start_pos, start_pos + seq_len_val), seq_len)
        batch_val = TensorValue(batch)
        slice_batch = (slice(0, batch_val), batch)
        k_cache[slice_seq_len, layer_index, slice_batch] = xk.transpose(0, 1).cast(
            k_cache.dtype
        )
        v_cache[slice_seq_len, layer_index, slice_batch] = xv.transpose(0, 1).cast(
            k_cache.dtype
        )

        # Then slice the correct keys and values for attention.
        # The cache can have a larger max batch size than the current input.
        # We slice down to the active batch size.
        # ... = cache[0:start_pos+seq_len, layer_index, :batch]
        slice_post_seq_len = (slice(0, start_pos + seq_len_val), "post_seq_len")
        keys = k_cache[slice_post_seq_len, layer_index, slice_batch].cast(xq.dtype)
        values = v_cache[slice_post_seq_len, layer_index, slice_batch].cast(xq.dtype)

        output = (
            self.attention(xq, xk, xv, attention_mask, keys, values)
            .transpose(1, 2)
            .reshape([batch, seq_len, -1])
        )
        return self.wo(output)
