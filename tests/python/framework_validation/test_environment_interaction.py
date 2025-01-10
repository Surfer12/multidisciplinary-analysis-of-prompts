"""Test module for validating environment interaction capabilities."""

import os
import sys
import pytest
import subprocess
from pathlib import Path

def test_environment_variables(temp_workspace):
    """Test environment variable operations."""
    # Set a test environment variable
    os.environ['TEST_VAR'] = 'test_value'

    # Verify environment variable
    assert os.getenv('TEST_VAR') == 'test_value'

    # Remove test variable
    del os.environ['TEST_VAR']
    assert os.getenv('TEST_VAR') is None

def test_python_path(temp_workspace):
    """Test Python path manipulation."""
    # Add temp workspace to Python path
    sys.path.insert(0, str(temp_workspace))

    # Create a test module
    module_dir = temp_workspace / "test_module"
    module_dir.mkdir()

    init_file = module_dir / "__init__.py"
    init_file.write_text("")

    test_file = module_dir / "test.py"
    test_file.write_text("""
def test_function():
    return "Test successful"
""")

    # Verify module can be imported
    sys.path.insert(0, str(temp_workspace))
    import test_module.test
    assert test_module.test.test_function() == "Test successful"

@pytest.mark.skipif(sys.platform != "darwin", reason="MacOS specific test")
def test_macos_specific(temp_workspace):
    """Test MacOS specific operations."""
    # Create a file with extended attributes
    test_file = temp_workspace / "test.txt"
    test_file.write_text("Test content")

    # Add extended attribute using xattr
    subprocess.run(['xattr', '-w', 'com.example.test', 'test_value', str(test_file)])

    # Read extended attribute
    result = subprocess.run(['xattr', '-p', 'com.example.test', str(test_file)],
                          capture_output=True, text=True)
    assert result.stdout.strip() == 'test_value'

def test_subprocess_execution(temp_workspace):
    """Test subprocess execution capabilities."""
    # Create a test script
    script_file = temp_workspace / "test_script.py"
    script_file.write_text("""
print("Hello from subprocess!")
""")

    # Execute script using subprocess
    result = subprocess.run([sys.executable, str(script_file)],
                          capture_output=True, text=True)

    assert result.stdout.strip() == "Hello from subprocess!"
    assert result.returncode == 0

class TestEnvironmentSetup:
    """Test class for environment setup operations."""

    def setup_method(self, method):
        """Set up test environment before each test method."""
        self.original_env = dict(os.environ)
        self.original_path = list(sys.path)

    def teardown_method(self, method):
        """Clean up test environment after each test method."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)

        # Restore original Python path
        sys.path[:] = self.original_path

    def test_environment_isolation(self, temp_workspace):
        """Test environment isolation capabilities."""
        # Modify environment
        os.environ['TEST_VAR'] = 'isolated_value'
        sys.path.append(str(temp_workspace))

        # Verify modifications
        assert os.getenv('TEST_VAR') == 'isolated_value'
        assert str(temp_workspace) in sys.path

        # Environment will be restored in teardown
