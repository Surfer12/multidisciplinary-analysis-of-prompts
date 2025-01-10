"""
Pattern visualization module for analyzing and visualizing cognitive patterns and tool usage.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, List, Any, Optional
import plotly.graph_objects as go
import networkx as nx

class PatternVisualizer:
    """Visualizer for cognitive patterns and tool usage analysis."""

    def __init__(self):
        """Initialize the visualizer with default style settings."""
        plt.style.use('seaborn')
        sns.set_theme(style="whitegrid")

    def plot_tool_usage_heatmap(self,
                               usage_data: pd.DataFrame,
                               title: str = "Tool Usage Patterns",
                               figsize: tuple = (12, 8)) -> None:
        """
        Create a heatmap visualization of tool usage patterns.

        Args:
            usage_data: DataFrame with tool usage data
            title: Plot title
            figsize: Figure size tuple (width, height)
        """
        plt.figure(figsize=figsize)
        sns.heatmap(usage_data,
                   annot=True,
                   cmap='YlOrRd',
                   fmt='.2f')
        plt.title(title)
        plt.xlabel('Time Period')
        plt.ylabel('Tool Name')
        plt.tight_layout()

    def create_cognitive_network(self,
                               nodes: List[str],
                               edges: List[tuple],
                               node_attrs: Optional[Dict[str, Any]] = None) -> go.Figure:
        """
        Create an interactive network visualization of cognitive patterns.

        Args:
            nodes: List of node names
            edges: List of (source, target) tuples
            node_attrs: Optional dictionary of node attributes

        Returns:
            Plotly figure object
        """
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        if node_attrs:
            nx.set_node_attributes(G, node_attrs)

        pos = nx.spring_layout(G)

        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlOrRd',
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                )
            )
        )

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)
            node_trace['text'] += (node,)

        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Cognitive Pattern Network',
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                       )

        return fig

    def plot_tool_performance(self,
                            performance_data: pd.DataFrame,
                            metric: str = 'execution_time',
                            figsize: tuple = (10, 6)) -> None:
        """
        Create a box plot visualization of tool performance metrics.

        Args:
            performance_data: DataFrame with tool performance data
            metric: Performance metric to visualize
            figsize: Figure size tuple (width, height)
        """
        plt.figure(figsize=figsize)
        sns.boxplot(data=performance_data,
                   x='tool_name',
                   y=metric)
        plt.title(f'Tool Performance Analysis: {metric}')
        plt.xticks(rotation=45)
        plt.tight_layout()

    def save_figure(self, filename: str, dpi: int = 300) -> None:
        """
        Save the current figure to a file.

        Args:
            filename: Output filename
            dpi: Resolution in dots per inch
        """
        plt.savefig(filename, dpi=dpi, bbox_inches='tight')
