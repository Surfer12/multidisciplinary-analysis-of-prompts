# Stable Diffusion inference with Python

This directory illustrates how to run Stable Diffusion through MAX Engine.
Specifically, this example extracts StableDiffusion-1.5 from Hugging Face and executes
it via the MAX Engine Python API.

## 🔒 Security Update

**IMPORTANT**: This example has been updated to address security concerns with pre-converted ONNX models.

### Changes Made:
- ✅ **Blocked risky models**: The previous model `modularai/stable-diffusion-1.5-onnx` has been flagged as potentially containing backdoors
- ✅ **Safe model conversion**: Now uses the official `runwayml/stable-diffusion-v1-5` model and converts it safely to ONNX format
- ✅ **Security validation**: Added model security validation and integrity checks
- ✅ **Automatic fallback**: If a risky model is detected, safe alternatives are automatically suggested

### Security Features:
- Model source validation against trusted repositories
- Automatic blocking of flagged models
- Safe PyTorch to ONNX conversion
- Model integrity validation
- Comprehensive security logging

## Quickstart

### 🔒 Security Migration (Required)

If you've used this example before, please run the security migration first:

```sh
# Install security dependencies
pip install -r requirements-security.txt

# Run the migration script
python migrate_to_secure.py
```

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
# Install security dependencies
pip install -r requirements-security.txt
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

## Files

### Core Files
- `text_to_image.py`: **Main program** that runs full stable-diffusion pipeline through MAX Engine with security validation
- `run.sh`: Shell script to run the example with proper environment setup

### Security Framework
- `security_config.py`: Security configuration with trusted/blocked model lists and validation functions
- `model_converter.py`: Safe model conversion utilities for PyTorch to ONNX conversion
- `migrate_to_secure.py`: Migration script to transition from risky models to secure alternatives
- `requirements-security.txt`: Additional dependencies for security features

### Configuration Files
- `environment.yml`: Conda environment configuration
- `pixi.toml`: Pixi package manager configuration
- `magic.lock`: Magic package lock file

### Security Features
- ✅ **Model validation**: Checks models against trusted sources before loading
- ✅ **Automatic blocking**: Prevents loading of flagged risky models
- ✅ **Safe conversion**: Converts PyTorch models to ONNX safely instead of using pre-converted models
- ✅ **Integrity checking**: Validates model file integrity where checksums are available
- ✅ **Comprehensive logging**: Detailed security event logging

### Migration from Previous Version
If you were using the previous version with `modularai/stable-diffusion-1.5-onnx`, this model has been blocked due to security concerns. The new version automatically uses `runwayml/stable-diffusion-v1-5` and converts it safely to ONNX format.
