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

"""
Secure Stable Diffusion Text-to-Image Generation

This version includes comprehensive model security validation to prevent
backdoor threats and ensure safe model execution.
"""

import signal
import sys
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from diffusers import PNDMScheduler
from max.engine import InferenceSession
from PIL import Image
from transformers import CLIPTokenizer

# Import our security validation module
from model_security import (
    download_and_validate_model,
    get_safe_alternative_models,
    SecurityException
)

DESCRIPTION = "Generate an image based on the given prompt with security validation."
GUIDANCE_SCALE_FACTOR = 7.5
LATENT_SCALE_FACTOR = 0.18215
OUTPUT_HEIGHT = 512
OUTPUT_WIDTH = 512
LATENT_WIDTH = OUTPUT_WIDTH // 8
LATENT_HEIGHT = OUTPUT_HEIGHT // 8
LATENT_CHANNELS = 4

# Default model (can be overridden with --model-id)
DEFAULT_MODEL_ID = "modularai/stable-diffusion-1.5-onnx"


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
    parser.add_argument(
        "--model-id",
        type=str,
        metavar="<model_id>",
        default=DEFAULT_MODEL_ID,
        help="HuggingFace model ID to use (default: modularai/stable-diffusion-1.5-onnx)",
    )
    parser.add_argument(
        "--strict-security",
        action="store_true",
        help="Enable strict security mode (blocks risky models)",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip model security validation (not recommended)",
    )
    parser.add_argument(
        "--list-safe-models",
        action="store_true",
        help="List known safe alternative models and exit",
    )
    parsed_args = parser.parse_args(args)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Set seed if requested.
    if parsed_args.seed:
        np.random.seed(parsed_args.seed)

    return parsed_args


def main():
    args = parse(sys.argv[1:])

    # List safe models if requested
    if args.list_safe_models:
        print("Known safe alternative models:")
        for model in get_safe_alternative_models():
            print(f"  - {model}")
        return

    # Security validation
    if not args.skip_validation:
        print("🔒 Starting model security validation...")
        try:
            model_dir, validation_results = download_and_validate_model(
                args.model_id, 
                strict_mode=args.strict_security
            )
            
            print(f"✅ Model validation completed for: {args.model_id}")
            print(f"   Safe to use: {validation_results['safe_to_use']}")
            
            if not validation_results['safe_to_use']:
                print("⚠️  WARNING: Model has security issues!")
                print("   Recommendations:")
                for rec in validation_results['recommendations']:
                    print(f"   - {rec}")
                
                if args.strict_security:
                    print("❌ Strict security mode enabled - blocking execution")
                    return
                else:
                    print("⚠️  Proceeding with caution (strict mode disabled)")
            
            # Show validation warnings if any
            if validation_results.get('file_validation', {}).get('warnings'):
                print("⚠️  Validation warnings:")
                for warning in validation_results['file_validation']['warnings']:
                    print(f"   - {warning}")
                    
        except SecurityException as e:
            print(f"❌ Security validation failed: {e}")
            print("\n💡 Suggestions:")
            print("   - Use --list-safe-models to see alternatives")
            print("   - Try a different model with --model-id")
            print("   - Use --skip-validation (not recommended)")
            return
        except Exception as e:
            print(f"❌ Validation error: {e}")
            if args.strict_security:
                print("❌ Strict security mode enabled - blocking execution")
                return
            else:
                print("⚠️  Proceeding without validation (strict mode disabled)")
                # Fall back to direct download
                from huggingface_hub import snapshot_download
                model_dir = Path(snapshot_download(args.model_id))
    else:
        print("⚠️  Skipping model security validation (not recommended)")
        from huggingface_hub import snapshot_download
        model_dir = Path(snapshot_download(args.model_id))

    # Compile & load models - this may take a few minutes.
    print("\n🔄 Loading and compiling models...")
    session = InferenceSession()
    txt_encoder = session.load(model_dir / "text_encoder" / "model.onnx")
    img_decoder = session.load(model_dir / "vae_decoder" / "model.onnx")
    img_diffuser = session.load(model_dir / "unet" / "model.onnx")
    print("✅ Models compiled.\n")

    # Instantiate tokenizer and scheduler.
    tokenizer = CLIPTokenizer.from_pretrained(model_dir / "tokenizer")
    scheduler = PNDMScheduler.from_pretrained(model_dir / "scheduler")

    # Run the stable diffusion pipeline
    run_stable_diffusion(
        args, txt_encoder, img_decoder, img_diffuser, tokenizer, scheduler
    )


if __name__ == "__main__":
    main()