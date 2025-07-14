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
Model Security Validation Module

This module provides security validation for ONNX models to detect potential
backdoor threats and ensure model safety before execution.
"""

import hashlib
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import onnx
from huggingface_hub import hf_hub_download, model_info
from huggingface_hub.utils import HfHubHTTPError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Known safe model hashes (should be maintained and updated)
SAFE_MODEL_HASHES = {
    "modularai/stable-diffusion-1.5-onnx": {
        "text_encoder/model.onnx": "sha256:...",  # Placeholder - needs actual hash
        "vae_decoder/model.onnx": "sha256:...",   # Placeholder - needs actual hash
        "unet/model.onnx": "sha256:...",          # Placeholder - needs actual hash
    }
}

# Known risky models (from HuggingFace security reports)
RISKY_MODELS = {
    "modularai/stable-diffusion-1.5-onnx": {
        "risk_level": "HIGH",
        "description": "Flagged as potentially containing backdoor threats",
        "recommendation": "Use alternative safe models or validate thoroughly"
    }
}


class ModelSecurityValidator:
    """Validates ONNX models for security threats and backdoors."""
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize the validator.
        
        Args:
            strict_mode: If True, blocks execution of risky models
        """
        self.strict_mode = strict_mode
        self.validation_results = {}
    
    def calculate_file_hash(self, file_path: Path, algorithm: str = "sha256") -> str:
        """Calculate hash of a file."""
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return f"{algorithm}:{hash_func.hexdigest()}"
    
    def validate_model_structure(self, model_path: Path) -> Dict[str, any]:
        """Validate ONNX model structure for suspicious patterns."""
        try:
            model = onnx.load(str(model_path))
            
            # Basic structure validation
            validation_result = {
                "valid": True,
                "warnings": [],
                "suspicious_patterns": []
            }
            
            # Check for unusual node types
            suspicious_ops = ["Custom", "Unknown", "Experimental"]
            for node in model.graph.node:
                if node.op_type in suspicious_ops:
                    validation_result["suspicious_patterns"].append(
                        f"Suspicious operation type: {node.op_type}"
                    )
                    validation_result["warnings"].append(
                        f"Found suspicious operation: {node.op_type}"
                    )
            
            # Check for unusually large models
            model_size = model_path.stat().st_size
            if model_size > 2 * 1024 * 1024 * 1024:  # 2GB
                validation_result["warnings"].append(
                    f"Model size is unusually large: {model_size / (1024**3):.2f}GB"
                )
            
            # Check for embedded strings that might contain malicious code
            for node in model.graph.node:
                for attr in node.attribute:
                    if attr.type == onnx.AttributeProto.STRING:
                        attr_value = attr.s.decode('utf-8', errors='ignore')
                        if any(suspicious in attr_value.lower() for suspicious in 
                               ['eval', 'exec', 'system', 'shell', 'backdoor']):
                            validation_result["suspicious_patterns"].append(
                                f"Suspicious string in attribute: {attr_value[:100]}..."
                            )
                            validation_result["warnings"].append(
                                "Found potentially malicious strings in model"
                            )
            
            return validation_result
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "warnings": ["Failed to load model for validation"]
            }
    
    def check_model_reputation(self, model_id: str) -> Dict[str, any]:
        """Check model reputation and security status."""
        try:
            info = model_info(model_id)
            
            # Check for security tags or warnings
            security_issues = []
            if hasattr(info, 'cardData') and info.cardData:
                card_data = info.cardData
                if isinstance(card_data, dict):
                    # Look for security-related metadata
                    if card_data.get('security', {}).get('flagged', False):
                        security_issues.append("Model flagged for security issues")
                    
                    if card_data.get('tags'):
                        tags = card_data['tags']
                        if any('security' in tag.lower() or 'risk' in tag.lower() 
                               for tag in tags):
                            security_issues.append("Model has security-related tags")
            
            return {
                "model_id": model_id,
                "security_issues": security_issues,
                "is_risky": model_id in RISKY_MODELS,
                "risk_info": RISKY_MODELS.get(model_id, {}),
                "downloads": getattr(info, 'downloads', 0),
                "likes": getattr(info, 'likes', 0)
            }
            
        except HfHubHTTPError as e:
            logger.warning(f"Could not fetch model info for {model_id}: {e}")
            return {
                "model_id": model_id,
                "security_issues": ["Could not verify model reputation"],
                "is_risky": model_id in RISKY_MODELS,
                "risk_info": RISKY_MODELS.get(model_id, {}),
                "downloads": 0,
                "likes": 0
            }
    
    def validate_model_files(self, model_dir: Path, model_id: str) -> Dict[str, any]:
        """Validate all model files in the directory."""
        validation_results = {
            "model_id": model_id,
            "overall_valid": True,
            "file_validations": {},
            "warnings": [],
            "errors": []
        }
        
        # Expected model files
        expected_files = [
            "text_encoder/model.onnx",
            "vae_decoder/model.onnx", 
            "unet/model.onnx"
        ]
        
        for file_path in expected_files:
            full_path = model_dir / file_path
            if not full_path.exists():
                validation_results["errors"].append(f"Missing expected file: {file_path}")
                validation_results["overall_valid"] = False
                continue
            
            # Calculate file hash
            file_hash = self.calculate_file_hash(full_path)
            
            # Validate model structure
            structure_validation = self.validate_model_structure(full_path)
            
            # Check against known safe hashes
            known_hash = SAFE_MODEL_HASHES.get(model_id, {}).get(file_path)
            hash_matches = known_hash == file_hash if known_hash else None
            
            validation_results["file_validations"][file_path] = {
                "hash": file_hash,
                "hash_matches_known": hash_matches,
                "structure_validation": structure_validation,
                "file_size": full_path.stat().st_size
            }
            
            if not structure_validation["valid"]:
                validation_results["overall_valid"] = False
                validation_results["errors"].append(
                    f"Structure validation failed for {file_path}"
                )
            
            if structure_validation["warnings"]:
                validation_results["warnings"].extend(
                    [f"{file_path}: {w}" for w in structure_validation["warnings"]]
                )
            
            if structure_validation["suspicious_patterns"]:
                validation_results["warnings"].extend(
                    [f"{file_path}: {p}" for p in structure_validation["suspicious_patterns"]]
                )
        
        return validation_results
    
    def run_netron_inspection(self, model_path: Path) -> Dict[str, any]:
        """Run Netron to inspect model structure (if available)."""
        try:
            # Check if netron is available
            result = subprocess.run(
                ["netron", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode != 0:
                return {
                    "available": False,
                    "error": "Netron not available"
                }
            
            # Run netron inspection
            result = subprocess.run(
                ["netron", "--port", "0", "--host", "localhost", str(model_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "available": True,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
            
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError) as e:
            return {
                "available": False,
                "error": str(e)
            }
    
    def validate_model_safety(self, model_id: str, model_dir: Path) -> Dict[str, any]:
        """
        Comprehensive model safety validation.
        
        Args:
            model_id: HuggingFace model ID
            model_dir: Path to downloaded model directory
            
        Returns:
            Validation results dictionary
        """
        logger.info(f"Starting security validation for model: {model_id}")
        
        # Check model reputation
        reputation = self.check_model_reputation(model_id)
        
        # Validate model files
        file_validation = self.validate_model_files(model_dir, model_id)
        
        # Run Netron inspection on one of the models
        sample_model = model_dir / "text_encoder" / "model.onnx"
        netron_inspection = {}
        if sample_model.exists():
            netron_inspection = self.run_netron_inspection(sample_model)
        
        # Compile results
        overall_result = {
            "model_id": model_id,
            "reputation_check": reputation,
            "file_validation": file_validation,
            "netron_inspection": netron_inspection,
            "recommendations": [],
            "safe_to_use": True
        }
        
        # Determine if model is safe to use
        if reputation["is_risky"]:
            overall_result["safe_to_use"] = False
            overall_result["recommendations"].append(
                "Model is flagged as risky - consider using alternative models"
            )
        
        if not file_validation["overall_valid"]:
            overall_result["safe_to_use"] = False
            overall_result["recommendations"].append(
                "Model file validation failed - do not use this model"
            )
        
        if file_validation["warnings"]:
            overall_result["recommendations"].append(
                "Model has validation warnings - review before use"
            )
        
        if reputation["security_issues"]:
            overall_result["recommendations"].append(
                "Model has security issues - proceed with caution"
            )
        
        # In strict mode, block risky models
        if self.strict_mode and not overall_result["safe_to_use"]:
            raise SecurityException(
                f"Model {model_id} failed security validation: "
                f"{overall_result['recommendations']}"
            )
        
        self.validation_results[model_id] = overall_result
        return overall_result


class SecurityException(Exception):
    """Exception raised when security validation fails."""
    pass


def get_safe_alternative_models() -> List[str]:
    """Get list of safe alternative models."""
    return [
        "runwayml/stable-diffusion-v1-5",  # Original model
        "CompVis/stable-diffusion-v1-4",   # Alternative version
        "stabilityai/stable-diffusion-2-1", # Newer version
    ]


def download_and_validate_model(model_id: str, strict_mode: bool = True) -> Tuple[Path, Dict]:
    """
    Download and validate a model for security.
    
    Args:
        model_id: HuggingFace model ID
        strict_mode: Whether to enforce strict security checks
        
    Returns:
        Tuple of (model_directory_path, validation_results)
    """
    from huggingface_hub import snapshot_download
    
    validator = ModelSecurityValidator(strict_mode=strict_mode)
    
    # Download model
    logger.info(f"Downloading model: {model_id}")
    model_dir = Path(snapshot_download(model_id))
    
    # Validate model
    validation_results = validator.validate_model_safety(model_id, model_dir)
    
    return model_dir, validation_results


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate model security")
    parser.add_argument("--model-id", default="modularai/stable-diffusion-1.5-onnx",
                       help="Model ID to validate")
    parser.add_argument("--strict", action="store_true", 
                       help="Enable strict security mode")
    parser.add_argument("--output", help="Output file for validation results")
    
    args = parser.parse_args()
    
    try:
        model_dir, results = download_and_validate_model(args.model_id, args.strict)
        print(f"Model validation completed for: {args.model_id}")
        print(f"Safe to use: {results['safe_to_use']}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Results saved to: {args.output}")
        else:
            print(json.dumps(results, indent=2, default=str))
            
    except SecurityException as e:
        print(f"Security validation failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Validation error: {e}")
        sys.exit(1)