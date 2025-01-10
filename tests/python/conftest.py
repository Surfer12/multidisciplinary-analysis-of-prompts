import pytest
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/python')))

@pytest.fixture
def test_data_dir():
    """Fixture providing path to test data directory."""
    return os.path.join(os.path.dirname(__file__), '..', 'data')

@pytest.fixture
def sample_config():
    """Fixture providing sample configuration for tests."""
    return {
        'project_root': os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')),
        'data_dir': 'data',
        'output_dir': 'output'
    }

@pytest.fixture
def temp_workspace(tmp_path):
    """Fixture providing a temporary workspace for tests."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace
