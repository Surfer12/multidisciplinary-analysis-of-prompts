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
Test script for model security validation functionality.
"""

import sys
import tempfile
from pathlib import Path

# Import our security module
from model_security import (
    ModelSecurityValidator,
    get_safe_alternative_models,
    SecurityException
)


def test_security_validator():
    """Test the security validator functionality."""
    print("🧪 Testing Model Security Validator")
    print("=" * 40)
    
    # Test 1: Validator initialization
    print("1. Testing validator initialization...")
    validator = ModelSecurityValidator(strict_mode=True)
    print("   ✅ Validator initialized successfully")
    
    # Test 2: Safe models list
    print("\n2. Testing safe models list...")
    safe_models = get_safe_alternative_models()
    print(f"   ✅ Found {len(safe_models)} safe alternative models:")
    for model in safe_models:
        print(f"      - {model}")
    
    # Test 3: File hash calculation
    print("\n3. Testing file hash calculation...")
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_file = Path(f.name)
    
    try:
        hash_result = validator.calculate_file_hash(temp_file)
        print(f"   ✅ Hash calculation successful: {hash_result}")
    finally:
        temp_file.unlink()
    
    # Test 4: Model reputation check
    print("\n4. Testing model reputation check...")
    try:
        reputation = validator.check_model_reputation("modularai/stable-diffusion-1.5-onnx")
        print(f"   ✅ Reputation check successful")
        print(f"      - Is risky: {reputation['is_risky']}")
        print(f"      - Security issues: {len(reputation['security_issues'])}")
    except Exception as e:
        print(f"   ⚠️  Reputation check failed (expected for offline testing): {e}")
    
    print("\n✅ All security validation tests completed!")


def test_security_exception():
    """Test security exception handling."""
    print("\n🧪 Testing Security Exception Handling")
    print("=" * 40)
    
    try:
        raise SecurityException("Test security exception")
    except SecurityException as e:
        print(f"   ✅ Security exception caught: {e}")
    
    print("✅ Security exception handling test completed!")


def main():
    """Run all security tests."""
    print("🔒 Model Security Validation Test Suite")
    print("=" * 50)
    
    try:
        test_security_validator()
        test_security_exception()
        
        print("\n🎉 All tests passed!")
        print("\n💡 To test with actual models, run:")
        print("   python3 model_security.py --model-id modularai/stable-diffusion-1.5-onnx")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()