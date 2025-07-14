#!/usr/bin/env python3
# ===----------------------------------------------------------------------=== #
# Copyright (c) 2024, Modular Inc. All rights reserved.
#
# Licensed under the Apache License 2.0 with LLVM Exceptions:
# https://llvm.org/LICENSE.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===----------------------------------------------------------------------=== #

"""
Checksum utilities for proper parsing of sha256sum files.

This module fixes the issue where filenames with spaces were incorrectly
parsed by using line.strip().split() which splits on any whitespace.
The sha256sum format uses two spaces as a delimiter before the filename.
"""

import hashlib
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def load_checksums(checksum_file: Path) -> Dict[str, str]:
    """
    Load checksums from a .sha256 file with proper handling of filenames containing spaces.
    
    The sha256sum format is: <hash>  <filename>
    where there are exactly two spaces between the hash and filename.
    
    Args:
        checksum_file: Path to the .sha256 file
        
    Returns:
        Dictionary mapping filenames to their SHA256 hashes
        
    Raises:
        FileNotFoundError: If the checksum file doesn't exist
        ValueError: If the checksum file format is invalid
    """
    if not checksum_file.exists():
        raise FileNotFoundError(f"Checksum file not found: {checksum_file}")
    
    checksums = {}
    
    with open(checksum_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse the line using regex to handle filenames with spaces
            # sha256sum format: <64-char-hex>  <filename>
            # Note: exactly two spaces between hash and filename
            match = re.match(r'^([a-fA-F0-9]{64})\s{2}(.+)$', line)
            
            if not match:
                raise ValueError(
                    f"Invalid checksum format at line {line_num}: {line}\n"
                    f"Expected format: <64-char-hex>  <filename>"
                )
            
            hash_value, filename = match.groups()
            
            # Normalize the filename (remove leading/trailing whitespace)
            filename = filename.strip()
            
            if not filename:
                raise ValueError(
                    f"Empty filename at line {line_num}: {line}"
                )
            
            checksums[filename] = hash_value.lower()
    
    return checksums


def verify_file_checksum(file_path: Path, expected_hash: str) -> bool:
    """
    Verify that a file matches its expected SHA256 hash.
    
    Args:
        file_path: Path to the file to verify
        expected_hash: Expected SHA256 hash (case-insensitive)
        
    Returns:
        True if the file matches the expected hash, False otherwise
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Calculate the actual hash
    actual_hash = calculate_file_hash(file_path)
    
    # Compare hashes (case-insensitive)
    return actual_hash.lower() == expected_hash.lower()


def calculate_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """
    Calculate the hash of a file.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (default: sha256)
        
    Returns:
        Hexadecimal hash string
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the algorithm is not supported
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        hash_func = hashlib.new(algorithm)
    except ValueError as e:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}") from e
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


def verify_checksums_against_files(checksum_file: Path, base_dir: Optional[Path] = None) -> Dict[str, bool]:
    """
    Verify all files listed in a checksum file against their actual hashes.
    
    Args:
        checksum_file: Path to the .sha256 file
        base_dir: Base directory for resolving relative filenames (default: checksum file directory)
        
    Returns:
        Dictionary mapping filenames to verification results (True = verified, False = failed)
        
    Raises:
        FileNotFoundError: If the checksum file doesn't exist
        ValueError: If the checksum file format is invalid
    """
    if base_dir is None:
        base_dir = checksum_file.parent
    
    checksums = load_checksums(checksum_file)
    results = {}
    
    for filename, expected_hash in checksums.items():
        file_path = base_dir / filename
        
        try:
            is_valid = verify_file_checksum(file_path, expected_hash)
            results[filename] = is_valid
        except FileNotFoundError:
            results[filename] = False
    
    return results


def create_checksum_file(files: List[Path], output_file: Path, base_dir: Optional[Path] = None) -> None:
    """
    Create a .sha256 checksum file for the given files.
    
    Args:
        files: List of file paths to include in the checksum file
        output_file: Path where the checksum file should be created
        base_dir: Base directory for creating relative filenames (default: output file directory)
        
    Raises:
        FileNotFoundError: If any of the input files don't exist
    """
    if base_dir is None:
        base_dir = output_file.parent
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for file_path in files:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Calculate hash
            hash_value = calculate_file_hash(file_path)
            
            # Create relative filename
            try:
                relative_path = file_path.relative_to(base_dir)
            except ValueError:
                # If file is not relative to base_dir, use absolute path
                relative_path = file_path
            
            # Write in sha256sum format: <hash>  <filename>
            f.write(f"{hash_value}  {relative_path}\n")


def test_checksum_parsing():
    """Test the checksum parsing functionality with various filename formats."""
    import tempfile
    
    # Create a test checksum file with various filename formats
    test_content = """# Test checksum file
a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678  simple_file.txt
b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890  file with spaces.txt
c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890ab  file/with/path.txt
d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890abcd  file with spaces and path/file.txt
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sha256', delete=False) as f:
        f.write(test_content)
        temp_file = Path(f.name)
    
    try:
        # Test parsing
        checksums = load_checksums(temp_file)
        
        # Verify expected results
        expected_files = [
            "simple_file.txt",
            "file with spaces.txt", 
            "file/with/path.txt",
            "file with spaces and path/file.txt"
        ]
        
        assert len(checksums) == 4, f"Expected 4 files, got {len(checksums)}"
        
        for filename in expected_files:
            assert filename in checksums, f"Missing file: {filename}"
            assert len(checksums[filename]) == 64, f"Invalid hash length for {filename}"
        
        print("✅ Checksum parsing test passed!")
        print(f"   Parsed {len(checksums)} files correctly")
        print(f"   Files with spaces handled properly: {list(checksums.keys())}")
        
    finally:
        temp_file.unlink()


if __name__ == "__main__":
    # Run tests if executed directly
    test_checksum_parsing()