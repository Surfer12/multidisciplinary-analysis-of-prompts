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
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from diffusers import PNDMScheduler
from huggingface_hub import snapshot_download
from max.engine import InferenceSession
from PIL import Image
from transformers import CLIPTokenizer

# -----------------------------------------------------------------------------
# Security-hardened Stable-Diffusion ONNX/Safetensors runner
# -----------------------------------------------------------------------------
# 1.  Requires an explicit `--model-id` (HF repo or local path).  No more
#     auto-downloading unvetted weights.
# 2.  Performs SHA-256 checksum verification if a JSON file named
#     `checksums.sha256` exists next to the downloaded snapshot *or* if the user
#     supplies `--checksum-file`.
# 3.  Runs `onnx.checker.check_model` on every *.onnx file before executing.
# 4.  Transparently supports loading *.safetensors weights when present.
# -----------------------------------------------------------------------------

DESCRIPTION = "Generate an image based on the given prompt (secure version)."
GUIDANCE_SCALE_FACTOR = 7.5
LATENT_SCALE_FACTOR = 0.18215
OUTPUT_HEIGHT = 512
OUTPUT_WIDTH = 512
LATENT_WIDTH = OUTPUT_WIDTH // 8
LATENT_HEIGHT = OUTPUT_HEIGHT // 8
LATENT_CHANNELS = 4

# -----------------------------------------------------------------------------
# Verification helpers
# -----------------------------------------------------------------------------

import hashlib
import json
from typing import Dict, Optional

try:
    import onnx  # noqa: F401 – only needed for validation; optional runtime dep.

    _HAS_ONNX = True
except ImportError:  # pragma: no cover – onnx optional in some envs
    _HAS_ONNX = False


def sha256(path: Path) -> str:
    """Return the hex SHA-256 of a file."""

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_checksums(checksum_file: Path) -> Dict[str, str]:
    """Load a mapping of relative paths -> sha256 from a JSON or .sha256 text."""

    if checksum_file.suffix == ".json":
        return json.loads(checksum_file.read_text())

    mapping: Dict[str, str] = {}
    for line in checksum_file.read_text().splitlines():
        if not line.strip():
            continue
        # common sha256sum format:  <hash> <two spaces> <filename>
        parts = line.strip().split()
        if len(parts) >= 2:
            mapping[parts[1]] = parts[0]
    return mapping


def verify_model_files(model_root: Path, checksum_db: Dict[str, str]):
    """Raise SystemExit if any checksum mismatch is detected."""

    if not checksum_db:
        print("⚠  No checksum data provided – skipping hash verification.")
        return

    print("Verifying model file integrity (SHA-256)…")
    for rel, expected_hash in checksum_db.items():
        file_path = model_root / rel
        if not file_path.exists():
            sys.exit(f"✖ Expected file {rel} is missing in {model_root}.")
        actual_hash = sha256(file_path)
        if actual_hash != expected_hash.lower():
            sys.exit(
                f"✖ Checksum mismatch for {rel}:\n"
                f"    expected {expected_hash.lower()}\n"
                f"    got      {actual_hash}"
            )
    print("✔  All files passed checksum verification.\n")


def validate_onnx_graph(model_path: Path):
    """Run onnx.checker on the graph; abort on failure."""

    if not _HAS_ONNX:
        print("⚠  onnx Python package not available – skipping ONNX validation.")
        return

    try:
        onnx.checker.check_model(model_path.as_posix())
    except Exception as e:  # broad but catches ValidationError & others
        sys.exit(f"✖ ONNX validation failed for {model_path.name}: {e}")

# -----------------------------------------------------------------------------


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
    # > Prompt & generation options ----------------------------------------------------------------
    parser.add_argument(
        "--prompt",
        type=str,
        metavar="<str>",
        required=True,
        help="Description of the desired image.",
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

    # > Model & security options -------------------------------------------------------------------
    parser.add_argument(
        "--model-id",
        type=str,
        metavar="<model|path>",
        required=True,
        help=(
            "HuggingFace repo ID or local directory containing the ONNX / "
            "safetensors pipeline. Example: modularai/stable-diffusion-1.5-onnx"
        ),
    )

    parser.add_argument(
        "--checksum-file",
        type=str,
        metavar="<path>",
        default=None,
        help="Optional .json or .sha256 file mapping relative model paths to sha256 \
              hashes for verification.",
    )

    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip onnx.checker validation (not recommended).",
    )

    parsed_args = parser.parse_args(args)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Set seed if requested.
    if parsed_args.seed is not None:
        np.random.seed(parsed_args.seed)

    return parsed_args


def main():
    args = parse(sys.argv[1:])

    # -------------------------------- Model acquisition --------------------------------------
    if Path(args.model_id).exists():
        model_dir = Path(args.model_id).expanduser().resolve()
    else:
        print("Downloading model snapshot from HuggingFace...")
        model_dir = Path(snapshot_download(args.model_id))

    # -------------------------------- Verification & validation ------------------------------
    checksum_db: Dict[str, str] = {}
    if args.checksum_file:
        checksum_db = load_checksums(Path(args.checksum_file))
    else:
        # If the repo ships a checksums.sha256 file, use it automatically.
        default_file = model_dir / "checksums.sha256"
        if default_file.exists():
            checksum_db = load_checksums(default_file)

    verify_model_files(model_dir, checksum_db)

    # -------------------------------- Model loading ------------------------------------------
    def find_weight_file(component_name: str) -> Path:
        comp_dir = model_dir / component_name
        for ext in (".safetensors", ".onnx"):
            candidate = comp_dir / f"model{ext}"
            if candidate.exists():
                if ext == ".onnx" and not args.skip_validation:
                    validate_onnx_graph(candidate)
                return candidate
        sys.exit(f"✖ No model.* file found for {component_name} in {comp_dir}.")

    session = InferenceSession()
    print("Loading and compiling models… (this may take a few minutes)")

    txt_encoder = session.load(find_weight_file("text_encoder"))
    img_decoder = session.load(find_weight_file("vae_decoder"))
    img_diffuser = session.load(find_weight_file("unet"))

    print("Models compiled and ready.\n")

    # -------------------------------- Aux modules --------------------------------------------
    tokenizer = CLIPTokenizer.from_pretrained(model_dir / "tokenizer")
    scheduler = PNDMScheduler.from_pretrained(model_dir / "scheduler")

    run_stable_diffusion(
        args, txt_encoder, img_decoder, img_diffuser, tokenizer, scheduler
    )


if __name__ == "__main__":
    main()
