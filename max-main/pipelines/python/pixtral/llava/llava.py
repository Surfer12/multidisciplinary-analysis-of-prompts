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

from dataclasses import dataclass

from max.graph import TensorValue, ops
from nn.layer import Layer
from pixtral.vision_encoder.vision_encoder import VisionEncoder

from .llava_decoder import Transformer
from .llava_projector import LlavaMultiModalConnector


@dataclass
class LlavaConditionalGeneration(Layer):
    """The LLAVA model which consists of a vision encoder and a language model.

    image_token_index: a specific token index used to denote images
    """

    vision_encoder: VisionEncoder
    multi_modal_projector: LlavaMultiModalConnector
    language_model: Transformer
    vocab_size: int
    image_token_index: int = 10
    vision_feature_layer: int = -1
    vision_feature_select_strategy: str = "full"
    image_seq_length: int = 1

    # TODO: change pixel_values type to List[TensorValue] to support multiple images.
    def __call__(
        self,
        input_ids: TensorValue,  # Shape (batch_size, sequence_length). Indices of input sequence tokens in the vocabulary. Indices can be obtained from language model tokenizer.
        pixel_values: TensorValue,  # (height, width, num_channels).
        kv_cache_inputs: tuple[TensorValue, TensorValue, TensorValue, TensorValue],
        **kwargs,
    ) -> TensorValue:
        """
        Args:
            input_ids (ragged `TensorValue` of shape `(batch_size * sequence_length for each batch)`):
                Indices of input sequence tokens in the vocabulary.
                input_ids[i] is a sequence of token ids (indices) in sequence i. Expanding inputs for
                image tokens in LLaVa should be done in processing. Each image is represented in the
                input_ids sequence by a sequence of patches that have index(id) = self.image_token_index.
                The maximum number of image tokens in one sequence (prompt) =
                    (input_ids == self.image_token_index).sum(1).max())
                Padding will be ignored by default should you provide it.
            pixel_values (`TensorValue` of shape `(batch_size, image_height, image_width, num_channels)):
                The tensors corresponding to the input images. Pixel values can be obtained using ImageProcessor
        """
        # TODO: if the input is a list, change vision_encoder input to pixel_values
        # Obtains image embeddings from the vision encoder.  Output shape = (num_images=batch_size, num_patches_in_image, vision_encoder_hidden_dim)
        # TODO: Works now for batch_size=1, Maybe convert to a ragged tensor to be compatible with input embeds?
        # Apply multimodal projection to  hidden states from the vision encoder. Output shape = (num_images, num_patches_in_image, language_model_hidden_dim)

        image_embeds = self.multi_modal_projector(
            self.vision_encoder(
                [
                    pixel_values,
                ]
            )
        )
        # inputs_embeds shape (total_sequence_length=text_and_image_tokens_length for all seqs,
        #   language_model_hidden_dim)
        inputs_embeds = self.language_model.embedding(input_ids)
        # Replace image place-holders in inputs_embeds with image embeddings.
        special_image_mask = ops.broadcast_to(
            ops.unsqueeze((input_ids == self.image_token_index), -1),
            inputs_embeds.shape,
        )
        image_embeds = ops.cast(image_embeds, inputs_embeds.dtype)
        inputs_embeds = ops.masked_scatter(
            inputs_embeds, special_image_mask, image_embeds
        )
        logits = self.language_model(inputs_embeds, kv_cache_inputs, **kwargs)
        return logits

        # max_tokens_per_image = (
        #     (input_ids == self.image_token_index).sum(1).max()
        # )
        # assert(max_tokens_per_image < self.image_seq_length)

        # n_image_embeds = n_images * n_patches_per_image
        # image_embeds.shape = [Dim(1), Dim(475), Dim(5120)]
        # n_image_embeds = image_embeds.shape[0] * image_embeds.shape[1]

        # n_image_tokens = ops.sum(ops.sum(ops.cast((input_ids == self.image_token_index), DType.int32)))[0]

        # if n_image_tokens != ops.constant(int(n_image_embeds), DType.int32):
        #     raise ValueError(
        #         "Image sfeatures and image tokens do not match: tokens:"
        #         f" {n_image_tokens}, features {n_image_embeds}"
        #     )
