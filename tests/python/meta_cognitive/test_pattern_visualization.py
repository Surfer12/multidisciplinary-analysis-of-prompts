"""Test module for pattern visualization capabilities."""

import pytest
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any
from .test_pattern_recognition import AdvancedPatternRecognizer, PatternType, PatternInstance

class PatternVisualizer:
    """Visualization tools for pattern analysis."""

    def __init__(self, pattern_recognizer: AdvancedPatternRecognizer):
        self.pattern_recognizer = pattern_recognizer
        plt.style.use('seaborn')

    def plot_pattern_distribution(self, save_path: str = None):
        """Plot the distribution of pattern types."""
        distribution = self.pattern_recognizer.analyze_pattern_distribution()
        type_dist = distribution['type_distribution']

        if not type_dist:
            return

        # Create bar plot
        plt.figure(figsize=(10, 6))
        plt.bar(type_dist.keys(), type_dist.values())
        plt.title('Pattern Type Distribution')
        plt.xlabel('Pattern Type')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

    def plot_confidence_distribution(self, save_path: str = None):
        """Plot the distribution of confidence scores."""
        confidences = [p.confidence for p in self.pattern_recognizer.pattern_history]
        if not confidences:
            return

        plt.figure(figsize=(10, 6))
        plt.hist(confidences, bins=20, edgecolor='black')
        plt.title('Pattern Confidence Distribution')
        plt.xlabel('Confidence Score')
        plt.ylabel('Frequency')

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

    def plot_pattern_evolution(self, save_path: str = None):
        """Plot the evolution of pattern recognition over time."""
        if not self.pattern_recognizer.pattern_history:
            return

        pattern_types = [p.pattern_type.name for p in self.pattern_recognizer.pattern_history]
        confidences = [p.confidence for p in self.pattern_recognizer.pattern_history]
        timestamps = range(len(pattern_types))

        plt.figure(figsize=(12, 6))
        scatter = plt.scatter(timestamps, confidences, c=[hash(pt) for pt in pattern_types])
        plt.title('Pattern Recognition Evolution')
        plt.xlabel('Pattern Sequence')
        plt.ylabel('Confidence Score')

        # Add legend
        unique_types = list(set(pattern_types))
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                    markerfacecolor=plt.cm.viridis(hash(t) % 256 / 256),
                                    label=t, markersize=10)
                         for t in unique_types]
        plt.legend(handles=legend_elements, title='Pattern Types')

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

    def plot_sub_pattern_network(self, save_path: str = None):
        """Plot network visualization of pattern relationships."""
        if not self.pattern_recognizer.pattern_history:
            return

        plt.figure(figsize=(12, 8))
        pos = {}
        edges = []

        # Create positions for main patterns
        for i, pattern in enumerate(self.pattern_recognizer.pattern_history):
            angle = 2 * np.pi * i / len(self.pattern_recognizer.pattern_history)
            pos[id(pattern)] = (np.cos(angle), np.sin(angle))

            # Add edges for sub-patterns
            for sub_pattern in pattern.sub_patterns:
                sub_angle = angle + np.random.uniform(-0.5, 0.5)
                radius = 0.5  # Shorter radius for sub-patterns
                pos[id(sub_pattern)] = (radius * np.cos(sub_angle),
                                      radius * np.sin(sub_angle))
                edges.append((id(pattern), id(sub_pattern)))

        # Plot nodes
        for node_id, position in pos.items():
            plt.plot(position[0], position[1], 'o')

        # Plot edges
        for edge in edges:
            start = pos[edge[0]]
            end = pos[edge[1]]
            plt.plot([start[0], end[0]], [start[1], end[1]], '-', alpha=0.5)

        plt.title('Pattern Relationship Network')
        plt.axis('equal')

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

@pytest.fixture
def pattern_visualizer(pattern_recognizer):
    """Fixture providing a PatternVisualizer instance."""
    return PatternVisualizer(pattern_recognizer)

def test_pattern_distribution_plot(pattern_visualizer, tmp_path):
    """Test plotting pattern type distribution."""
    # Generate test patterns
    for _ in range(20):
        pattern_visualizer.pattern_recognizer.recognize_pattern(
            "Test data",
            {'source': 'test', 'iteration': _}
        )

    # Test plotting
    save_path = tmp_path / "pattern_distribution.png"
    pattern_visualizer.plot_pattern_distribution(str(save_path))
    assert save_path.exists()

def test_confidence_distribution_plot(pattern_visualizer, tmp_path):
    """Test plotting confidence score distribution."""
    # Generate test patterns
    for _ in range(20):
        pattern_visualizer.pattern_recognizer.recognize_pattern(
            "Test data",
            {'source': 'test', 'iteration': _}
        )

    # Test plotting
    save_path = tmp_path / "confidence_distribution.png"
    pattern_visualizer.plot_confidence_distribution(str(save_path))
    assert save_path.exists()

def test_pattern_evolution_plot(pattern_visualizer, tmp_path):
    """Test plotting pattern evolution over time."""
    # Generate test patterns
    for _ in range(20):
        pattern_visualizer.pattern_recognizer.recognize_pattern(
            "Test data",
            {'source': 'test', 'iteration': _}
        )

    # Test plotting
    save_path = tmp_path / "pattern_evolution.png"
    pattern_visualizer.plot_pattern_evolution(str(save_path))
    assert save_path.exists()

def test_sub_pattern_network_plot(pattern_visualizer, tmp_path):
    """Test plotting sub-pattern network."""
    # Generate test patterns with sub-patterns
    for _ in range(10):
        pattern_visualizer.pattern_recognizer.recognize_pattern(
            "Complex test data",
            {'source': 'test', 'complexity': 0.8}
        )

    # Test plotting
    save_path = tmp_path / "pattern_network.png"
    pattern_visualizer.plot_sub_pattern_network(str(save_path))
    assert save_path.exists()
