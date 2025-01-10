"""
Interactive dashboard for visualizing cognitive patterns and tool usage.
"""
import streamlit as st
import pandas as pd
import numpy as np
from pattern_viz import PatternVisualizer

def load_sample_data():
    """Load sample data for demonstration."""
    # Tool usage data
    tools = ['Tool A', 'Tool B', 'Tool C', 'Tool D']
    periods = ['Period 1', 'Period 2', 'Period 3', 'Period 4']
    usage_data = pd.DataFrame(
        np.random.rand(len(tools), len(periods)),
        index=tools,
        columns=periods
    )

    # Performance data
    tools_perf = tools * 10
    metrics = np.random.rand(40)
    performance_data = pd.DataFrame({
        'tool_name': tools_perf,
        'execution_time': metrics
    })

    # Cognitive network data
    nodes = ['Concept A', 'Concept B', 'Concept C', 'Concept D']
    edges = [
        ('Concept A', 'Concept B'),
        ('Concept B', 'Concept C'),
        ('Concept C', 'Concept D'),
        ('Concept A', 'Concept D')
    ]

    return usage_data, performance_data, nodes, edges

def main():
    """Main function to run the Streamlit dashboard."""
    st.title("Cognitive Pattern Analysis Dashboard")

    # Initialize visualizer
    viz = PatternVisualizer()

    # Load sample data
    usage_data, performance_data, nodes, edges = load_sample_data()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a visualization:",
        ["Tool Usage Patterns", "Performance Analysis", "Cognitive Network"]
    )

    if page == "Tool Usage Patterns":
        st.header("Tool Usage Patterns")
        st.write("Heatmap showing tool usage patterns over time")

        # Plot heatmap
        fig_size = st.slider(
            "Select figure size",
            min_value=6,
            max_value=20,
            value=12
        )
        viz.plot_tool_usage_heatmap(usage_data, figsize=(fig_size, fig_size * 0.6))
        st.pyplot()

    elif page == "Performance Analysis":
        st.header("Tool Performance Analysis")
        st.write("Box plot showing performance metrics for different tools")

        # Plot performance
        metric = st.selectbox(
            "Select performance metric",
            ["execution_time"]
        )
        viz.plot_tool_performance(performance_data, metric=metric)
        st.pyplot()

    else:  # Cognitive Network
        st.header("Cognitive Network Visualization")
        st.write("Interactive network showing relationships between concepts")

        # Create and display network
        fig = viz.create_cognitive_network(nodes, edges)
        st.plotly_chart(fig)

    # Additional options
    st.sidebar.header("Options")
    if st.sidebar.button("Export Visualizations"):
        # Add export functionality here
        st.sidebar.write("Export functionality to be implemented")

    # About section
    st.sidebar.markdown("---")
    st.sidebar.header("About")
    st.sidebar.info(
        """
        This dashboard provides interactive visualizations for analyzing cognitive patterns
        and tool usage in the system. Use the navigation menu to explore different aspects
        of the analysis.
        """
    )

if __name__ == "__main__":
    main()
