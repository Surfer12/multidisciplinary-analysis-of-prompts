"""Security configuration for model loading and validation."""
import logging
from typing import List, Dict, Optional
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)

# List of trusted model sources for Stable Diffusion
TRUSTED_MODEL_SOURCES = [
    "runwayml/stable-diffusion-v1-5",
    "CompVis/stable-diffusion-v1-4",
    "stabilityai/stable-diffusion-2-1",
    "stabilityai/stable-diffusion-xl-base-1.0",
    # Add more verified safe models as needed
]

# Models that are known to be risky and should be blocked
BLOCKED_MODELS = [
    "modularai/stable-diffusion-1.5-onnx",  # Flagged for security issues
    # Add other known risky models
]

# Expected checksums for model validation (example format)
EXPECTED_CHECKSUMS = {
    "runwayml/stable-diffusion-v1-5": {
        "unet/diffusion_pytorch_model.safetensors": "expected_hash_here",
        "vae/diffusion_pytorch_model.safetensors": "expected_hash_here",
        # Add more checksums as needed
    }
}

def is_model_trusted(model_id: str) -> bool:
    """Check if a model is from a trusted source."""
    return model_id in TRUSTED_MODEL_SOURCES and model_id not in BLOCKED_MODELS

def is_model_blocked(model_id: str) -> bool:
    """Check if a model is explicitly blocked."""
    return model_id in BLOCKED_MODELS

def validate_model_security(model_id: str) -> tuple[bool, str]:
    """
    Validate model security status.
    
    Returns:
        tuple: (is_safe, message)
    """
    if is_model_blocked(model_id):
        return False, f"Model {model_id} is blocked due to security concerns"
    
    if is_model_trusted(model_id):
        return True, f"Model {model_id} is from a trusted source"
    
    return False, f"Model {model_id} is not in the trusted sources list"

def get_security_warning(model_id: str) -> str:
    """Get security warning message for a model."""
    if is_model_blocked(model_id):
        return (
            f"🚨 SECURITY WARNING: Model '{model_id}' is blocked due to known security issues. "
            "Please use an alternative trusted model."
        )
    
    if not is_model_trusted(model_id):
        return (
            f"⚠️  SECURITY NOTICE: Model '{model_id}' is not in the trusted sources list. "
            "Please verify the model's safety before using it in production."
        )
    
    return ""

def validate_model_integrity(model_dir: Path, model_id: str) -> bool:
    """
    Validate model file integrity using checksums.
    
    Args:
        model_dir: Path to the model directory
        model_id: Model identifier
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    if model_id not in EXPECTED_CHECKSUMS:
        logger.warning(f"No checksums available for model {model_id}")
        return True  # Allow if no checksums are defined
    
    expected_checksums = EXPECTED_CHECKSUMS[model_id]
    
    for file_path, expected_hash in expected_checksums.items():
        file_full_path = model_dir / file_path
        
        if not file_full_path.exists():
            logger.error(f"Expected file not found: {file_full_path}")
            return False
        
        actual_hash = hashlib.sha256(file_full_path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            logger.error(f"Hash mismatch for {file_path}: expected {expected_hash}, got {actual_hash}")
            return False
    
    return True

def recommend_safe_alternative(blocked_model: str) -> Optional[str]:
    """Recommend a safe alternative for a blocked model."""
    alternatives = {
        "modularai/stable-diffusion-1.5-onnx": "runwayml/stable-diffusion-v1-5",
    }
    return alternatives.get(blocked_model)