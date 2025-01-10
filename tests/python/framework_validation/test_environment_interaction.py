"""Tests for environment interaction functionality."""
import os
import sys


def test_environment_setup():
    """Test basic environment configuration."""
    assert sys.version_info >= (3, 8), "Python version must be 3.8 or higher"
    assert "PYTHONPATH" in os.environ, "PYTHONPATH should be set"
