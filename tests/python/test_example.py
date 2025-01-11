"""Example test module demonstrating test structure and pytest features."""

import os

import pytest


def test_workspace_creation(temp_workspace):
    """Test that the temporary workspace fixture works correctly."""
    assert temp_workspace.exists()
    assert temp_workspace.is_dir()


def test_config_structure(sample_config):
    """Test that the sample configuration fixture provides expected structure."""
    assert 'project_root' in sample_config
    assert 'data_dir' in sample_config
    assert 'output_dir' in sample_config


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("test1", "TEST1"),
        ("test2", "TEST2"),
        ("test3", "TEST3"),
    ],
)
def test_parameterized_example(test_input, expected):
    """Demonstrate parameterized testing."""
    assert test_input.upper() == expected


class TestExampleClass:
    """Example test class demonstrating class-based testing."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.test_data = ["item1", "item2", "item3"]

    def test_list_manipulation(self):
        """Test basic list operations."""
        self.test_data.append("item4")
        assert len(self.test_data) == 4
        assert "item4" in self.test_data

    def test_list_removal(self):
        """Test removing items from list."""
        self.test_data.remove("item2")
        assert len(self.test_data) == 2
        assert "item2" not in self.test_data
