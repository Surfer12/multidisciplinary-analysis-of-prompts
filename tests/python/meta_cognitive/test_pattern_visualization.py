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


@pytest.fixture(autouse=True)
def setup_matplotlib():
    """Configure matplotlib for testing."""
    plt.switch_backend('Agg')  # Use non-interactive backend
    yield
    plt.close('all')  # Cleanup after each test


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

    # Test with invalid data
    with pytest.raises(ValueError, match="Usage data cannot be empty"):
        visualizer.plot_tool_usage_heatmap(pd.DataFrame())

    # Test with non-numeric data
    invalid_data = pd.DataFrame({'A': ['a', 'b'], 'B': ['c', 'd']})
    with pytest.raises(ValueError, match="All data must be numeric"):
        visualizer.plot_tool_usage_heatmap(invalid_data)


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

    # Test with empty nodes
    with pytest.raises(ValueError, match="Node list cannot be empty"):
        visualizer.create_cognitive_network([], edges)

    # Test with empty edges
    with pytest.raises(ValueError, match="Edge list cannot be empty"):
        visualizer.create_cognitive_network(nodes, [])

    # Test with invalid edge
    invalid_edges = [("Node A", "Node D")]  # Node D doesn't exist
    with pytest.raises(ValueError, match="references non-existent node"):
        visualizer.create_cognitive_network(nodes, invalid_edges)


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

    # Test with empty data
    with pytest.raises(ValueError, match="Performance data cannot be empty"):
        visualizer.plot_tool_performance(pd.DataFrame())

    # Test with missing required columns
    invalid_data = pd.DataFrame({"wrong_column": [1, 2, 3]})
    with pytest.raises(ValueError, match="Missing required columns"):
        visualizer.plot_tool_performance(invalid_data)


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

    # Test with empty filename
    with pytest.raises(ValueError, match="Filename cannot be empty"):
        visualizer.save_figure("")
