"""Test module for advanced computer operations and meta-cognitive capabilities."""

import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

import psutil
import pytest
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileChangeHandler(FileSystemEventHandler):
    """Handler for file system changes."""

    def __init__(self):
        self.changes = []

    def on_modified(self, event):
        if not event.is_directory:
            self.changes.append(('modified', event.src_path))

    def on_created(self, event):
        if not event.is_directory:
            self.changes.append(('created', event.src_path))


@pytest.fixture
def file_watcher():
    """Fixture providing a file system watcher."""
    handler = FileChangeHandler()
    observer = Observer()
    return handler, observer


def test_process_management(temp_workspace):
    """Test process creation, monitoring, and termination."""
    # Create a long-running script
    script_path = temp_workspace / "long_running.py"
    script_path.write_text(
        """
import time
while True:
    time.sleep(1)
"""
    )

    # Start process
    process = subprocess.Popen(
        [sys.executable, str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Get process info
    proc = psutil.Process(process.pid)

    # Verify process is running
    assert proc.is_running()
    assert proc.status() == psutil.STATUS_RUNNING

    # Check resource usage
    cpu_percent = proc.cpu_percent(interval=0.1)
    memory_info = proc.memory_info()

    assert isinstance(cpu_percent, float)
    assert memory_info.rss > 0

    # Terminate process
    process.terminate()
    process.wait(timeout=5)

    # Verify process has ended
    assert not proc.is_running()


def test_file_system_monitoring(temp_workspace, file_watcher):
    """Test real-time file system monitoring."""
    handler, observer = file_watcher

    # Start watching the directory
    observer.schedule(handler, str(temp_workspace), recursive=False)
    observer.start()

    try:
        # Create new file
        test_file = temp_workspace / "monitored.txt"
        test_file.write_text("Initial content")

        # Give watcher time to process
        time.sleep(1)

        # Modify file
        test_file.write_text("Modified content")

        # Give watcher time to process
        time.sleep(1)

        # Verify changes were detected
        changes = handler.changes
        assert len(changes) >= 2
        assert ('created', str(test_file)) in changes
        assert ('modified', str(test_file)) in changes

    finally:
        observer.stop()
        observer.join()


def test_resource_monitoring():
    """Test system resource monitoring capabilities."""
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    assert isinstance(cpu_percent, float)
    assert 0 <= cpu_percent <= 100

    # Memory usage
    memory = psutil.virtual_memory()
    assert memory.total > 0
    assert memory.available > 0
    assert memory.percent >= 0

    # Disk usage
    disk = psutil.disk_usage('/')
    assert disk.total > 0
    assert disk.used > 0
    assert disk.free > 0

    # Network interfaces
    network_interfaces = psutil.net_if_addrs()
    assert len(network_interfaces) > 0


def test_parallel_file_operations(temp_workspace):
    """Test parallel file operations and synchronization."""
    # Create shared counter
    counter = {'value': 0}
    lock = threading.Lock()

    def worker(worker_id):
        """Worker function for parallel operations."""
        for i in range(10):
            # Create worker-specific file
            file_path = temp_workspace / f"worker_{worker_id}_file_{i}.txt"
            file_path.write_text(f"Content from worker {worker_id}")

            # Update shared counter
            with lock:
                counter['value'] += 1

    # Create and start threads
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Verify results
    assert counter['value'] == 50  # 5 workers * 10 files each

    # Check all files exist
    file_count = len(list(temp_workspace.glob("worker_*_file_*.txt")))
    assert file_count == 50


@pytest.mark.skipif(sys.platform != "darwin", reason="MacOS specific test")
def test_macos_advanced_features(temp_workspace):
    """Test advanced MacOS-specific features."""
    # Create a test file
    test_file = temp_workspace / "advanced_test.txt"
    test_file.write_text("Test content")

    # Test file flags
    subprocess.run(['chflags', 'hidden', str(test_file)])

    # Verify file is hidden
    result = subprocess.run(
        ['ls', '-lO', str(test_file)], capture_output=True, text=True
    )
    assert 'hidden' in result.stdout.lower()

    # Test file metadata
    subprocess.run(
        ['xattr', '-w', 'com.apple.metadata:kMDLabel_1', 'TestLabel', str(test_file)]
    )

    # Verify metadata
    result = subprocess.run(
        ['xattr', '-l', str(test_file)], capture_output=True, text=True
    )
    assert 'com.apple.metadata:kMDLabel_1' in result.stdout


class TestAdvancedEnvironment:
    """Test class for advanced environment operations."""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Set up and tear down test environment."""
        # Store original state
        self.original_env = dict(os.environ)
        self.original_cwd = os.getcwd()

        yield

        # Restore original state
        os.environ.clear()
        os.environ.update(self.original_env)
        os.chdir(self.original_cwd)

    def test_complex_environment(self, temp_workspace):
        """Test complex environment manipulations."""
        # Create nested directory structure
        (temp_workspace / "dir1" / "dir2" / "dir3").mkdir(parents=True)

        # Change working directory
        os.chdir(temp_workspace / "dir1" / "dir2")

        # Set up environment variables
        os.environ.update(
            {
                'TEST_VAR1': 'value1',
                'TEST_VAR2': 'value2',
                'TEST_PATH': os.pathsep.join(
                    [
                        str(temp_workspace / "bin"),
                        str(temp_workspace / "usr/local/bin"),
                        os.environ.get('PATH', ''),
                    ]
                ),
            }
        )

        # Verify environment
        assert os.getcwd().endswith('dir2')
        assert os.environ['TEST_VAR1'] == 'value1'
        assert os.environ['TEST_VAR2'] == 'value2'
        assert str(temp_workspace / "bin") in os.environ['TEST_PATH']
