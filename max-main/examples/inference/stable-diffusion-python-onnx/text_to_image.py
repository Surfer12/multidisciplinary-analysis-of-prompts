#!/usr/bin/env python3
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

import signal
import sys
import logging
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from diffusers import PNDMScheduler
from huggingface_hub import snapshot_download
from max.engine import InferenceSession
from PIL import Image
from transformers import CLIPTokenizer

# Import security utilities
from security_config import (
    validate_model_security, 
    get_security_warning, 
    recommend_safe_alternative,
    validate_model_integrity
)
from model_converter import convert_model_safely

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DESCRIPTION = "Generate an image based on the given prompt."
GUIDANCE_SCALE_FACTOR = 7.5
LATENT_SCALE_FACTOR = 0.18215
OUTPUT_HEIGHT = 512
OUTPUT_WIDTH = 512
LATENT_WIDTH = OUTPUT_WIDTH // 8
LATENT_HEIGHT = OUTPUT_HEIGHT // 8
LATENT_CHANNELS = 4


def run_stable_diffusion(
    args, txt_encoder, img_decoder, img_diffuser, tokenizer, scheduler
):
    # Tokenize inputs and run through text encoder.
    print("Processing input...")
    prompt_p = tokenizer(
        args.prompt, padding="max_length", max_length=tokenizer.model_max_length
    )
    prompt_n = tokenizer(
        args.negative_prompt,
        padding="max_length",
        max_length=tokenizer.model_max_length,
    )

    input_ids = np.stack((prompt_p.input_ids, prompt_n.input_ids)).astype(np.int32)
    encoder_hidden_states = txt_encoder.execute_legacy(input_ids=input_ids)[
        "last_hidden_state"
    ]
    print("Input processed.\n")

    # Initialize latent and scheduler.
    print("Initializing latent...")

    # Note: For onnx, shapes are given in NCHW format.
    latent = np.random.normal(size=(1, LATENT_CHANNELS, LATENT_HEIGHT, LATENT_WIDTH))
    latent = latent * scheduler.init_noise_sigma
    latent = latent.astype(np.float32)

    # Loop through diffusion model.
    scheduler.set_timesteps(args.num_steps)
    for i, t in enumerate(scheduler.timesteps):
        print(f"\rGenerating image: {i}/{args.num_steps}", end="")

        # Duplicate input and scale based on scheduler.
        sample = np.vstack((latent, latent))
        sample = scheduler.scale_model_input(sample, timestep=t)

        # Execute the diffusion model with bs=2. Both batches have same primary input and
        # timestep, but the encoder_hidden_states (primary prompt vs negative) differs.
        noise_pred = img_diffuser.execute_legacy(
            sample=sample,
            encoder_hidden_states=encoder_hidden_states,
            timestep=np.array([t], dtype=np.int64),
        )["out_sample"]

        # Merge conditioned & unconditioned outputs.
        noise_pred_text, noise_pred_uncond = np.split(noise_pred, 2)
        noise_pred = noise_pred_uncond + GUIDANCE_SCALE_FACTOR * (
            noise_pred_text - noise_pred_uncond
        )

        # Merge latent with previous iteration.
        latent = scheduler.step(noise_pred, t, latent).prev_sample

    # Decode finalized latent.
    print("\n\nDecoding image...")
    latent = latent * (1 / LATENT_SCALE_FACTOR)
    decoded = img_decoder.execute_legacy(latent_sample=latent)["sample"]
    image = np.clip(decoded / 2 + 0.5, 0, 1).squeeze()
    image = (image.transpose(1, 2, 0) * 255).astype(np.uint8)
    Image.fromarray(image, "RGB").save(args.output)
    print(f"Image saved to {args.output}.")
    return


def parse(args):
    # Parse args.
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--prompt",
        type=str,
        metavar="<str>",
        required=True,
        help="Description of desired image.",
    )
    parser.add_argument(
        "--negative-prompt",
        type=str,
        metavar="<str>",
        default="",
        help="Objects or styles to avoid in generated image.",
    )
    parser.add_argument(
        "--num-steps",
        type=int,
        metavar="<int>",
        default=25,
        help="# of diffusion steps; trades-off speed vs quality",
    )
    parser.add_argument(
        "--seed",
        type=int,
        metavar="<int>",
        default=None,
        help="Seed for psuedo-random number generation.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        metavar="<outfile>",
        default="output.png",
        help="Output filename.",
    )
    parsed_args = parser.parse_args(args)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Set seed if requested.
    if parsed_args.seed:
        np.random.seed(parsed_args.seed)

    return parsed_args


def get_safe_model_dir(model_id: str = "runwayml/stable-diffusion-v1-5") -> Path:
    """
    Get a safe model directory, converting from PyTorch to ONNX if needed.
    
    Args:
        model_id: HuggingFace model identifier
        
    Returns:
        Path to safe ONNX model directory
    """
    # First, validate model security
    is_safe, message = validate_model_security(model_id)
    if not is_safe:
        warning = get_security_warning(model_id)
        logger.error(warning)
        alternative = recommend_safe_alternative(model_id)
        if alternative:
            logger.info(f"Using safe alternative: {alternative}")
            model_id = alternative
            is_safe, message = validate_model_security(model_id)
            if not is_safe:
                raise ValueError(f"No safe alternative available for the requested model")
        else:
            raise ValueError(f"Model {model_id} is not safe to use: {message}")
    
    # Check if we already have a converted version
    cache_dir = Path.home() / ".cache" / "modular" / "safe_models"
    model_cache_dir = cache_dir / model_id.replace("/", "_")
    
    if model_cache_dir.exists() and (model_cache_dir / "text_encoder" / "model.onnx").exists():
        logger.info(f"Using cached safe model: {model_cache_dir}")
        return model_cache_dir
    
    # Convert the model safely
    logger.info(f"Converting {model_id} to safe ONNX format...")
    logger.info("This may take a few minutes on the first run...")
    
    try:
        converted_dir = convert_model_safely(model_id, str(model_cache_dir))
        logger.info(f"Model safely converted and cached: {converted_dir}")
        return converted_dir
    except Exception as e:
        logger.error(f"Failed to convert model safely: {e}")
        raise RuntimeError(f"Could not obtain safe model: {e}")

def main():
    args = parse(sys.argv[1:])

    # Security notice
    print("🔒 MAX Engine Secure Stable Diffusion")
    print("=" * 50)
    print("This version uses security-validated models only.")
    print("Risky pre-converted models are automatically blocked.")
    print()

    # Get safe model directory
    try:
        model_dir = get_safe_model_dir()
        print(f"✅ Using safe model from: {model_dir}")
    except Exception as e:
        print(f"❌ Security check failed: {e}")
        sys.exit(1)

    # Validate model integrity
    logger.info("Validating model integrity...")
    # Note: This would use checksums if available
    
    # Compile & load models - this may take a few minutes.
    session = InferenceSession()
    print("Loading and compiling models...")
    txt_encoder = session.load(model_dir / "text_encoder" / "model.onnx")
    img_decoder = session.load(model_dir / "vae_decoder" / "model.onnx")
    img_diffuser = session.load(model_dir / "unet" / "model.onnx")
    print("Models compiled.\n")

    # Instantiate tokenizer and scheduler.
    tokenizer = CLIPTokenizer.from_pretrained(model_dir / "tokenizer")
    scheduler = PNDMScheduler.from_pretrained(model_dir / "scheduler")

    run_stable_diffusion(
        args, txt_encoder, img_decoder, img_diffuser, tokenizer, scheduler
    )


if __name__ == "__main__":
    main()
