"""
Example workflows demonstrating meta-cognitive capabilities in the computer use demo.
"""

import asyncio
from datetime import datetime
from typing import Dict, List

from cognitive_framework.tools.meta_cognitive import (
    MetaCognitiveToolCollection,
    MetaComputerTool,
    MetaCognitiveState
)

async def pattern_recognition_workflow():
    """Demonstrate pattern recognition capabilities."""
    # Initialize tools with pattern analysis enabled
    tool_collection = MetaCognitiveToolCollection(
        MetaComputerTool(),
        config={
            "observation": {
                "state_tracking": True,
                "pattern_analysis": True
            },
            "adaptation": {
                "enabled": False
            }
        }
    )

    # Execute a series of related actions
    actions = [
        {"action": "take_screenshot", "x": 100, "y": 100, "width": 500, "height": 500},
        {"action": "take_screenshot", "x": 100, "y": 100, "width": 500, "height": 500},
        {"action": "click", "x": 250, "y": 250},
        {"action": "take_screenshot", "x": 100, "y": 100, "width": 500, "height": 500}
    ]

    patterns = []
    for action in actions:
        result = await tool_collection.run("computer", action)
        if hasattr(result, "patterns"):
            patterns.extend(result.patterns)

    # Analyze patterns
    screenshot_patterns = [p for p in patterns if "screenshot" in str(p)]
    click_patterns = [p for p in patterns if "click" in str(p)]

    print("Pattern Analysis Results:")
    print(f"Screenshot Patterns: {len(screenshot_patterns)}")
    print(f"Click Patterns: {len(click_patterns)}")

    return patterns

async def adaptive_execution_workflow():
    """Demonstrate adaptive execution capabilities."""
    # Initialize tools with adaptation enabled
    tool_collection = MetaCognitiveToolCollection(
        MetaComputerTool(),
        config={
            "observation": {
                "state_tracking": True,
                "pattern_analysis": True
            },
            "adaptation": {
                "enabled": True,
                "threshold": 0.7
            }
        }
    )

    # Execute actions that might trigger adaptations
    actions = [
        # Initial action
        {"action": "take_screenshot", "x": 0, "y": 0, "width": 1000, "height": 1000},

        # Action that might be resource intensive
        {"action": "take_screenshot", "x": 0, "y": 0, "width": 2000, "height": 2000},

        # Action after potential adaptation
        {"action": "take_screenshot", "x": 0, "y": 0, "width": 1500, "height": 1500}
    ]

    adaptations = []
    for action in actions:
        result = await tool_collection.run("computer", action)
        if hasattr(result, "adaptations"):
            adaptations.extend(result.adaptations)

    print("\nAdaptation Results:")
    for adaptation in adaptations:
        print(f"Type: {adaptation['type']}")
        if "reason" in adaptation:
            print(f"Reason: {adaptation['reason']}")

    return adaptations

async def performance_monitoring_workflow():
    """Demonstrate performance monitoring capabilities."""
    # Initialize tools with comprehensive monitoring
    tool_collection = MetaCognitiveToolCollection(
        MetaComputerTool(),
        config={
            "observation": {
                "state_tracking": True,
                "pattern_analysis": True,
                "performance_monitoring": True
            },
            "adaptation": {
                "enabled": True,
                "threshold": 0.7
            }
        }
    )

    # Execute actions while monitoring performance
    actions = [
        {"action": "click", "x": 100, "y": 100},
        {"action": "take_screenshot", "x": 0, "y": 0, "width": 800, "height": 600},
        {"action": "click", "x": 200, "y": 200},
        {"action": "take_screenshot", "x": 0, "y": 0, "width": 800, "height": 600}
    ]

    metrics_history = []
    for action in actions:
        result = await tool_collection.run("computer", action)
        if hasattr(result, "metrics"):
            metrics_history.append({
                "timestamp": datetime.now().isoformat(),
                "action": action["action"],
                "metrics": result.metrics
            })

    print("\nPerformance Metrics:")
    for entry in metrics_history:
        print(f"\nTimestamp: {entry['timestamp']}")
        print(f"Action: {entry['action']}")
        for metric, value in entry['metrics'].items():
            print(f"{metric}: {value}")

    return metrics_history

async def integrated_workflow():
    """Demonstrate all meta-cognitive capabilities working together."""
    # Initialize tools with all features enabled
    tool_collection = MetaCognitiveToolCollection(
        MetaComputerTool(),
        config={
            "observation": {
                "state_tracking": True,
                "pattern_analysis": True,
                "performance_monitoring": True
            },
            "adaptation": {
                "enabled": True,
                "threshold": 0.7
            }
        }
    )

    # Complex sequence of actions
    actions = [
        # Initial exploration
        {"action": "click", "x": 100, "y": 100},
        {"action": "take_screenshot", "x": 0, "y": 0, "width": 800, "height": 600},

        # Repeated pattern
        {"action": "click", "x": 200, "y": 200},
        {"action": "take_screenshot", "x": 0, "y": 0, "width": 800, "height": 600},
        {"action": "click", "x": 300, "y": 300},
        {"action": "take_screenshot", "x": 0, "y": 0, "width": 800, "height": 600},

        # Resource-intensive action
        {"action": "take_screenshot", "x": 0, "y": 0, "width": 2000, "height": 2000}
    ]

    workflow_results = {
        "patterns": [],
        "adaptations": [],
        "metrics": []
    }

    for action in actions:
        result = await tool_collection.run("computer", action)

        # Collect patterns
        if hasattr(result, "patterns"):
            workflow_results["patterns"].extend(result.patterns)

        # Collect adaptations
        if hasattr(result, "adaptations"):
            workflow_results["adaptations"].extend(result.adaptations)

        # Collect metrics
        if hasattr(result, "metrics"):
            workflow_results["metrics"].append({
                "timestamp": datetime.now().isoformat(),
                "action": action["action"],
                "metrics": result.metrics
            })

    print("\nIntegrated Workflow Results:")
    print(f"\nPatterns Detected: {len(workflow_results['patterns'])}")
    print(f"Adaptations Made: {len(workflow_results['adaptations'])}")
    print(f"Metrics Collected: {len(workflow_results['metrics'])}")

    return workflow_results

async def main():
    """Run all example workflows."""
    print("Running Pattern Recognition Workflow...")
    patterns = await pattern_recognition_workflow()

    print("\nRunning Adaptive Execution Workflow...")
    adaptations = await adaptive_execution_workflow()

    print("\nRunning Performance Monitoring Workflow...")
    metrics = await performance_monitoring_workflow()

    print("\nRunning Integrated Workflow...")
    integrated_results = await integrated_workflow()

if __name__ == "__main__":
    asyncio.run(main())
