"""Test module for validating computer interaction capabilities."""

import os
from pathlib import Path

import pytest


def test_file_creation(temp_workspace):
    """Test creating a file and verifying its contents."""
    test_file = temp_workspace / "test.txt"
    test_content = "Hello, Computer!"

    # Write content to file
    test_file.write_text(test_content)

    # Verify file exists and contains correct content
    assert test_file.exists()
    assert test_file.read_text() == test_content


def test_directory_operations(temp_workspace):
    """Test directory creation and navigation."""
    # Create nested directories
    test_dir = temp_workspace / "test_dir" / "nested_dir"
    test_dir.mkdir(parents=True)

    # Create a file in the nested directory
    test_file = test_dir / "nested_file.txt"
    test_file.write_text("Nested content")

    # Verify directory structure
    assert test_dir.exists()
    assert test_dir.is_dir()
    assert test_file.exists()
    assert test_file.read_text() == "Nested content"


def test_file_manipulation(temp_workspace):
    """Test file manipulation operations."""
    # Create initial file
    source_file = temp_workspace / "source.txt"
    source_file.write_text("Original content")

    # Create a copy
    target_file = temp_workspace / "target.txt"
    target_file.write_text(source_file.read_text())

    # Modify source file
    source_file.write_text("Modified content")

    # Verify files are different
    assert source_file.read_text() != target_file.read_text()
    assert target_file.read_text() == "Original content"
    assert source_file.read_text() == "Modified content"


@pytest.mark.parametrize(
    "file_name,content",
    [
        ("test1.txt", "Content 1"),
        ("test2.txt", "Content 2"),
        ("test3.txt", "Content 3"),
    ],
)
def test_multiple_files(temp_workspace, file_name, content):
    """Test handling multiple files with different contents."""
    test_file = temp_workspace / file_name
    test_file.write_text(content)

    assert test_file.exists()
    assert test_file.read_text() == content


def test_file_deletion(temp_workspace):
    """Test file deletion capabilities."""
    # Create and then delete a file
    test_file = temp_workspace / "to_delete.txt"
    test_file.write_text("Delete me")

    assert test_file.exists()
    test_file.unlink()
    assert not test_file.exists()


class TestFileSystem:
    """Test class for file system operations."""

    def setup_method(self, method):
        """Set up test environment before each test method."""
        self.test_files = []

    def teardown_method(self, method):
        """Clean up test environment after each test method."""
        for file in self.test_files:
            if file.exists():
                file.unlink()

    def test_file_system_operations(self, temp_workspace):
        """Test comprehensive file system operations."""
        # Create multiple files
        for i in range(3):
            test_file = temp_workspace / f"file_{i}.txt"
            test_file.write_text(f"Content {i}")
            self.test_files.append(test_file)

        # Verify all files exist
        for i, file in enumerate(self.test_files):
            assert file.exists()
            assert file.read_text() == f"Content {i}"

        # Modify files
        for i, file in enumerate(self.test_files):
            file.write_text(f"Modified {i}")

        # Verify modifications
        for i, file in enumerate(self.test_files):
            assert file.read_text() == f"Modified {i}"
