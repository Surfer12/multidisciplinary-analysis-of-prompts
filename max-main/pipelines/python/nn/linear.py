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

"""Multi-layer Perceptron."""

from __future__ import annotations

from dataclasses import dataclass

from max.graph import Device, TensorValue, TensorValueLike, Weight, ops

from .kernels import swish_glu
from .layer import Layer


@dataclass
class Linear(Layer):
    """A fully connected layer."""

    weight: TensorValueLike
    bias: TensorValueLike | None = None

    def __call__(self, x: TensorValue) -> TensorValue:
        weight = TensorValue(self.weight)
        if (
            isinstance(self.weight, Weight)
            and self.weight.quantization_encoding is not None
        ):
            res = ops.qmatmul(self.weight.quantization_encoding, x, weight)
            if self.bias is not None:
                res += TensorValue(self.bias)
            return res

        res = x @ weight.T
        if self.bias is not None:
            res += TensorValue(self.bias)
        return res


@dataclass
class MLP(Layer):
    """
    Simple multi-layer perceptron composed of three linear layers.
    Uses SiLU activation function.
    """

    gate_proj: Linear
    down_proj: Linear
    up_proj: Linear

    def __call__(self, x: TensorValueLike) -> TensorValue:
        if (
            self.gate_proj.bias is None
            and self.up_proj.bias is None
            and TensorValue(x).rank == 2
            and TensorValue(x).device is not None
            and TensorValue(x).device != Device.CPU()
            and False  # GEX-1476: This causes elaboration errors - disable swish_glu pathway.
        ):
            return self.down_proj(
                swish_glu(
                    x,
                    self.gate_proj.weight,
                    self.up_proj.weight,
                )
            )

        return self.down_proj((ops.silu(self.gate_proj(x)) * self.up_proj(x)))  # type: ignore
