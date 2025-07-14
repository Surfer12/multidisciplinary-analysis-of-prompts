# Stable Diffusion inference with Python

This directory illustrates how to run Stable Diffusion through MAX Engine.
Specifically, this example extracts StableDiffusion-1.5 from Hugging Face and executes
it via the MAX Engine Python API.

## ⚠️ Security Notice

**IMPORTANT**: The default model `modularai/stable-diffusion-1.5-onnx` has been flagged as potentially containing backdoor threats on HuggingFace. 

**For production use, we strongly recommend:**
- Using the secure version: `text_to_image_secure.py`
- Using alternative safe models (see SECURITY.md)
- Enabling strict security validation

See [SECURITY.md](SECURITY.md) for detailed security information and mitigation strategies.

## Quickstart

### Magic instructions

If you have [`magic`](https://docs.modular.com/magic), you can run the
following command:

```sh
magic run bash run.sh
```

### Conda instructions

Create a Conda environment, activate that environment, and install the
requirements:

```sh
# Create a Conda environment if you don't have one
conda create -n max-repo
# Update the environment with the environment.yml file
conda env update -n max-repo -f environment.yml --prune
# Run the example
conda run -n max-repo --live-stream bash run.sh
```

## Custom Images

Getting started with your own creative prompts is as simple as:

```sh
./text_to_image.py --prompt "my image description" -o my-image.png
```

But of course, there are some additional settings that can be tweaked for more
fine-grained control over image output. See `./text_to_image.py --help` for
details.

## 🔒 Secure Usage (Recommended)

For production environments or when security is a concern, use the secure version:

```sh
# Use secure version with validation
./text_to_image_secure.py --prompt "my image description" --strict-security

# Or use the secure run script
./run_secure.sh

# List safe alternative models
./text_to_image_secure.py --list-safe-models
```

The secure version includes:
- Model security validation
- Backdoor threat detection
- Hash verification
- Reputation checking
- Strict mode enforcement

## Files

- `download-model.py`: Downloads [runwayml/stable-diffusion-v1-5
](https://huggingface.co/runwayml/stable-diffusion-v1-5)
and exports it as ONNX.

- `text_to_image.py`: Example program that runs full stable-diffusion pipeline
through MAX Engine in order to generate images from the given prompt.

- `text_to_image_secure.py`: **Secure version** with comprehensive model validation and backdoor threat detection.

- `model_security.py`: Security validation module for ONNX models.

- `run_secure.sh`: Secure run script with validation enabled.

- `SECURITY.md`: Comprehensive security documentation and guidelines.
