"""Tests for pattern visualization functionality."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

from src.visualization.pattern_viz import PatternVisualizer


@pytest.fixture
def visualizer():
    """Create a PatternVisualizer instance for testing."""
    return PatternVisualizer()


def test_plot_tool_usage_heatmap(visualizer):
    """Test creation of tool usage heatmap."""
    # Create sample data
    data = pd.DataFrame(
        np.random.rand(3, 4),
        index=["Tool A", "Tool B", "Tool C"],
        columns=["Period 1", "Period 2", "Period 3", "Period 4"],
    )

    # Test with default parameters
    visualizer.plot_tool_usage_heatmap(data)
    plt.close()

    # Test with custom parameters
    visualizer.plot_tool_usage_heatmap(data, title="Custom Title", figsize=(8, 6))
    plt.close()


def test_create_cognitive_network(visualizer):
    """Test creation of cognitive network visualization."""
    nodes = ["Node A", "Node B", "Node C"]
    edges = [("Node A", "Node B"), ("Node B", "Node C")]

    # Test with default parameters
    fig = visualizer.create_cognitive_network(nodes, edges)
    assert fig is not None

    # Test with node attributes
    node_attrs = {"Node A": {"weight": 1}, "Node B": {"weight": 2}}
    fig = visualizer.create_cognitive_network(nodes, edges, node_attrs)
    assert fig is not None


def test_plot_tool_performance(visualizer):
    """Test creation of tool performance visualization."""
    # Create sample data
    data = pd.DataFrame(
        {
            "tool_name": ["Tool A", "Tool B", "Tool C"] * 5,
            "execution_time": np.random.rand(15),
        }
    )

    # Test with default parameters
    visualizer.plot_tool_performance(data)
    plt.close()

    # Test with custom parameters
    visualizer.plot_tool_performance(data, metric="execution_time", figsize=(8, 6))
    plt.close()


def test_save_figure(visualizer, tmp_path):
    """Test figure saving functionality."""
    # Create a simple plot
    plt.figure()
    # Create a simple colormap
    colors = [(0, 0, 0), (1, 0, 0)]  # Black to red
    cmap = LinearSegmentedColormap.from_list("custom", colors)
    line = Line2D([0, 1], [0, 1], color=cmap(0.5))
    plt.gca().add_line(line)

    # Save figure
    output_file = tmp_path / "test_figure.png"
    visualizer.save_figure(str(output_file))
    assert output_file.exists()
    plt.close()


def test_error_handling(visualizer):
    """Test error handling in visualization methods."""
    # Test with invalid data
    with pytest.raises(Exception):
        visualizer.plot_tool_usage_heatmap(pd.DataFrame())

    with pytest.raises(Exception):
        visualizer.create_cognitive_network([], [])

    with pytest.raises(Exception):
        visualizer.plot_tool_performance(pd.DataFrame())

    # Test save_figure with invalid path
    with pytest.raises(Exception):
        visualizer.save_figure("")
