"""Safe model conversion utilities for Stable Diffusion."""
import logging
import torch
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
from diffusers import StableDiffusionPipeline
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers.models import AutoencoderKL, UNet2DConditionModel
import onnx
import onnxruntime as ort
from huggingface_hub import snapshot_download
from security_config import validate_model_security, get_security_warning, recommend_safe_alternative

logger = logging.getLogger(__name__)

class SafeModelConverter:
    """Safely convert PyTorch models to ONNX format."""
    
    def __init__(self, model_id: str, output_dir: Path):
        """
        Initialize the converter.
        
        Args:
            model_id: HuggingFace model identifier
            output_dir: Directory to save converted models
        """
        self.model_id = model_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate model security
        is_safe, message = validate_model_security(model_id)
        if not is_safe:
            warning = get_security_warning(model_id)
            logger.error(warning)
            alternative = recommend_safe_alternative(model_id)
            if alternative:
                logger.info(f"Consider using this safe alternative: {alternative}")
            raise ValueError(f"Model {model_id} is not safe to use: {message}")
    
    def convert_text_encoder(self, text_encoder: CLIPTextModel) -> Path:
        """Convert text encoder to ONNX."""
        output_path = self.output_dir / "text_encoder" / "model.onnx"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create dummy input
        dummy_input = torch.randint(0, 1000, (1, 77), dtype=torch.long)
        
        # Export to ONNX
        torch.onnx.export(
            text_encoder,
            dummy_input,
            output_path,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=['input_ids'],
            output_names=['last_hidden_state', 'pooler_output'],
            dynamic_axes={
                'input_ids': {0: 'batch_size'},
                'last_hidden_state': {0: 'batch_size'},
                'pooler_output': {0: 'batch_size'}
            }
        )
        
        logger.info(f"Text encoder converted to {output_path}")
        return output_path
    
    def convert_unet(self, unet: UNet2DConditionModel) -> Path:
        """Convert UNet to ONNX."""
        output_path = self.output_dir / "unet" / "model.onnx"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create dummy inputs
        sample = torch.randn(2, 4, 64, 64)
        timestep = torch.tensor([1])
        encoder_hidden_states = torch.randn(2, 77, 768)
        
        # Export to ONNX
        torch.onnx.export(
            unet,
            (sample, timestep, encoder_hidden_states),
            output_path,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=['sample', 'timestep', 'encoder_hidden_states'],
            output_names=['out_sample'],
            dynamic_axes={
                'sample': {0: 'batch_size', 2: 'height', 3: 'width'},
                'encoder_hidden_states': {0: 'batch_size'},
                'out_sample': {0: 'batch_size', 2: 'height', 3: 'width'}
            }
        )
        
        logger.info(f"UNet converted to {output_path}")
        return output_path
    
    def convert_vae_decoder(self, vae: AutoencoderKL) -> Path:
        """Convert VAE decoder to ONNX."""
        output_path = self.output_dir / "vae_decoder" / "model.onnx"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create dummy input
        latent_sample = torch.randn(1, 4, 64, 64)
        
        # Extract only the decoder part
        class VAEDecoder(torch.nn.Module):
            def __init__(self, vae):
                super().__init__()
                self.vae = vae
            
            def forward(self, latent_sample):
                return self.vae.decode(latent_sample).sample
        
        vae_decoder = VAEDecoder(vae)
        
        # Export to ONNX
        torch.onnx.export(
            vae_decoder,
            latent_sample,
            output_path,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=['latent_sample'],
            output_names=['sample'],
            dynamic_axes={
                'latent_sample': {0: 'batch_size', 2: 'height', 3: 'width'},
                'sample': {0: 'batch_size', 2: 'height', 3: 'width'}
            }
        )
        
        logger.info(f"VAE decoder converted to {output_path}")
        return output_path
    
    def validate_onnx_model(self, onnx_path: Path) -> bool:
        """Validate converted ONNX model."""
        try:
            # Load and check ONNX model
            onnx_model = onnx.load(str(onnx_path))
            onnx.checker.check_model(onnx_model)
            
            # Test with ONNX Runtime
            providers = ['CPUExecutionProvider']
            session = ort.InferenceSession(str(onnx_path), providers=providers)
            
            logger.info(f"ONNX model validation passed: {onnx_path}")
            return True
            
        except Exception as e:
            logger.error(f"ONNX model validation failed for {onnx_path}: {e}")
            return False
    
    def convert_full_pipeline(self) -> Path:
        """Convert entire Stable Diffusion pipeline to ONNX."""
        logger.info(f"Converting {self.model_id} to ONNX format...")
        
        # Load the original PyTorch model
        pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float32,
            use_safetensors=True
        )
        
        # Convert each component
        text_encoder_path = self.convert_text_encoder(pipe.text_encoder)
        unet_path = self.convert_unet(pipe.unet)
        vae_decoder_path = self.convert_vae_decoder(pipe.vae)
        
        # Validate all converted models
        if not all([
            self.validate_onnx_model(text_encoder_path),
            self.validate_onnx_model(unet_path),
            self.validate_onnx_model(vae_decoder_path)
        ]):
            raise RuntimeError("ONNX model validation failed")
        
        # Copy tokenizer and scheduler configs
        self._copy_configs(pipe)
        
        logger.info(f"Full pipeline conversion completed: {self.output_dir}")
        return self.output_dir
    
    def _copy_configs(self, pipe: StableDiffusionPipeline):
        """Copy tokenizer and scheduler configurations."""
        # Copy tokenizer
        tokenizer_dir = self.output_dir / "tokenizer"
        tokenizer_dir.mkdir(exist_ok=True)
        pipe.tokenizer.save_pretrained(tokenizer_dir)
        
        # Copy scheduler
        scheduler_dir = self.output_dir / "scheduler"
        scheduler_dir.mkdir(exist_ok=True)
        pipe.scheduler.save_pretrained(scheduler_dir)
        
        logger.info("Tokenizer and scheduler configs copied")

def convert_model_safely(model_id: str, output_dir: str) -> Path:
    """
    Safely convert a PyTorch model to ONNX format.
    
    Args:
        model_id: HuggingFace model identifier
        output_dir: Directory to save converted models
        
    Returns:
        Path to converted model directory
    """
    converter = SafeModelConverter(model_id, Path(output_dir))
    return converter.convert_full_pipeline()

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python model_converter.py <model_id> <output_dir>")
        sys.exit(1)
    
    model_id = sys.argv[1]
    output_dir = sys.argv[2]
    
    try:
        converted_path = convert_model_safely(model_id, output_dir)
        print(f"Model successfully converted to: {converted_path}")
    except Exception as e:
        print(f"Conversion failed: {e}")
        sys.exit(1)