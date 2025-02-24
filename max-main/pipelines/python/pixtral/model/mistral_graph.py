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
"""Build a Mistral model via Graph API from Safetensor weights."""

from max.dtype import DType
from max.graph import Graph, ops
from max.graph.weights import SafetensorWeights
from max.pipelines import PipelineConfig
from max.pipelines.kv_cache import (
    FetchContinuousBatchingKVCacheCollection,
    KVCacheParams,
)
from nn import (
    MLP,
    AttentionWithRope,
    Embedding,
    Linear,
    OptimizedRotaryEmbedding,
    RMSNorm,
    TransformerBlock,
)

from ..llava.llava_decoder import Transformer


def feed_forward(
    dtype: DType,
    hidden_dim: int,
    feed_forward_length: int,
    weights: SafetensorWeights,
):
    return MLP(
        linear(
            dtype,
            feed_forward_length,
            hidden_dim,
            weights.mlp.gate_proj,
        ),
        linear(
            dtype,
            hidden_dim,
            feed_forward_length,
            weights.mlp.down_proj,
        ),
        linear(
            dtype,
            feed_forward_length,
            hidden_dim,
            weights.mlp.up_proj,
        ),
    )


def linear(
    dtype: DType,
    in_features: int,
    out_features: int,
    weights: SafetensorWeights,
) -> Linear:
    return Linear(weights.weight.allocate(dtype, [in_features, out_features], None))


def rms_norm(dims: int, eps: float, weights: SafetensorWeights) -> RMSNorm:
    return RMSNorm(weights.weight.allocate(DType.bfloat16, [dims]), eps)


def embedding(
    params: PipelineConfig,
    vocab_size: int,
    hidden_dim: int,
    weights: SafetensorWeights,
):
    return Embedding(
        weights.weight.allocate(
            params.dtype,
            [vocab_size, hidden_dim],
        )
    )


def _attention_opaque(
    kv_params: KVCacheParams,
    params: PipelineConfig,
    rope: OptimizedRotaryEmbedding,
    weights: SafetensorWeights,
    layer_idx: int,
):
    kv_weight_dim = (
        params.huggingface_config.text_config.head_dim
        * params.huggingface_config.text_config.num_key_value_heads
    )

    wq = ops.transpose(
        weights.self_attn.q_proj.weight.allocate(
            params.dtype,
            [
                params.huggingface_config.text_config.num_attention_heads
                * params.huggingface_config.text_config.head_dim,
                params.huggingface_config.text_config.hidden_size,
            ],
        ),
        0,
        1,
    )
    wk = ops.transpose(
        weights.self_attn.k_proj.weight.allocate(
            params.dtype,
            [kv_weight_dim, params.huggingface_config.text_config.hidden_size],
        ),
        0,
        1,
    )
    wv = ops.transpose(
        weights.self_attn.v_proj.weight.allocate(
            params.dtype,
            [kv_weight_dim, params.huggingface_config.text_config.hidden_size],
        ),
        0,
        1,
    )
    wqkv = ops.concat((wq, wk, wv), axis=1).transpose(0, 1)

    return AttentionWithRope(
        n_heads=params.huggingface_config.text_config.num_attention_heads,
        kv_params=kv_params,
        wqkv=wqkv,
        wo=linear(
            params.dtype,
            params.huggingface_config.text_config.hidden_size,
            params.huggingface_config.text_config.num_attention_heads
            * params.huggingface_config.text_config.head_dim,
            weights.self_attn.o_proj,
        ),
        rope=rope,
        layer_idx=layer_idx,  # type: ignore
    )


def _transformer(
    graph: Graph,
    params: PipelineConfig,
    weights: SafetensorWeights,
    kv_params: KVCacheParams,
):
    with graph:
        rope = OptimizedRotaryEmbedding(
            dim=params.huggingface_config.text_config.num_attention_heads
            * params.huggingface_config.text_config.head_dim,
            n_heads=params.huggingface_config.text_config.num_attention_heads,
            theta=params.huggingface_config.text_config.rope_theta,
            max_seq_len=params.max_length,
            rope_scaling=None,
        )

        layers = [
            TransformerBlock(
                attention=_attention_opaque(
                    kv_params,
                    params,
                    rope,
                    weights.language_model.model.layers[i],
                    layer_idx=ops.constant(i, DType.uint32),  # type: ignore
                ),
                mlp=feed_forward(
                    params.dtype,
                    params.huggingface_config.text_config.hidden_size,
                    params.huggingface_config.text_config.intermediate_size,
                    weights.language_model.model.layers[i],
                ),
                attention_norm=rms_norm(
                    params.huggingface_config.text_config.hidden_size,
                    params.huggingface_config.text_config.rms_norm_eps,
                    weights.language_model.model.layers[i].post_attention_layernorm,
                ),
                mlp_norm=rms_norm(
                    params.huggingface_config.text_config.hidden_size,
                    params.huggingface_config.text_config.rms_norm_eps,
                    weights.language_model.model.layers[i].input_layernorm,
                ),
            )
            for i in range(params.huggingface_config.text_config.num_hidden_layers)
        ]

        embedding_layer = embedding(
            params,
            params.huggingface_config.text_config.vocab_size,
            params.huggingface_config.text_config.hidden_size,
            weights.language_model.model.embed_tokens,
        )

        output = Linear(embedding_layer.weights)

        kv_collection_cls = FetchContinuousBatchingKVCacheCollection

        return Transformer(
            dim=params.huggingface_config.text_config.hidden_size,
            n_heads=params.huggingface_config.text_config.num_attention_heads,
            layers=layers,
            norm=rms_norm(
                params.huggingface_config.text_config.hidden_size,
                params.huggingface_config.text_config.rms_norm_eps,
                weights.language_model.model.norm,
            ),
            output=output,
            embedding=embedding_layer,
            kv_params=kv_params,
            kv_collection_constructor=kv_collection_cls(kv_params),
        )
