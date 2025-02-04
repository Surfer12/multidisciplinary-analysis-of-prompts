"""Tests for the pattern visualization module."""
import numpy as np
import pandas as pd
import pytest

from visualization.pattern_viz import PatternVisualizer


@pytest.fixture
def visualizer():
    """Create a PatternVisualizer instance for testing."""
    return PatternVisualizer()


@pytest.fixture
def sample_usage_data():
    """Create sample tool usage data for testing."""
    tools = ['Tool A', 'Tool B', 'Tool C']
    periods = ['Period 1', 'Period 2', 'Period 3']
    data = np.random.rand(len(tools), len(periods))
    return pd.DataFrame(data, index=tools, columns=periods)


@pytest.fixture
def sample_performance_data():
    """Create sample performance data for testing."""
    tools = ['Tool A', 'Tool B', 'Tool C'] * 10
    metrics = np.random.rand(30)
    return pd.DataFrame({'tool_name': tools, 'execution_time': metrics})


def test_plot_tool_usage_heatmap(visualizer, sample_usage_data):
    """Test creation of tool usage heatmap."""
    visualizer.plot_tool_usage_heatmap(sample_usage_data)
    # Basic test to ensure no exceptions are raised
    assert True


def test_create_cognitive_network(visualizer):
    """Test creation of cognitive network visualization."""
    nodes = ['Node A', 'Node B', 'Node C']
    edges = [('Node A', 'Node B'), ('Node B', 'Node C')]
    fig = visualizer.create_cognitive_network(nodes, edges)
    assert fig is not None
    assert len(fig.data) == 2  # Edge trace and node trace


def test_plot_tool_performance(visualizer, sample_performance_data):
    """Test creation of tool performance visualization."""
    visualizer.plot_tool_performance(sample_performance_data)
    # Basic test to ensure no exceptions are raised
    assert True


def test_save_figure(visualizer, sample_usage_data, tmp_path):
    """Test figure saving functionality."""
    output_file = tmp_path / "test_figure.png"
    visualizer.plot_tool_usage_heatmap(sample_usage_data)
    visualizer.save_figure(str(output_file))
    assert output_file.exists()
