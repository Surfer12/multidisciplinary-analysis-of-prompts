"""Tests for monitoring and pattern detection capabilities."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from computer_use_demo.monitoring import PrometheusMonitoring, MonitoringIntegration
from computer_use_demo.tools.computer import PatternDetector
from computer_use_demo.tools.base import MetaCognitiveState, TimeSeriesMetrics

@pytest.fixture
def pattern_detector():
    return PatternDetector()

@pytest.fixture
def monitoring():
    with patch('prometheus_client.start_http_server'):
        return PrometheusMonitoring(port=8000)

@pytest.mark.asyncio
async def test_pattern_detection(pattern_detector):
    # Test repetitive action detection
    operation_type = "mouse_click"
    context = {"x": 100, "y": 100}

    # Add multiple similar operations
    for _ in range(4):
        pattern_detector.patterns.append({
            "action": operation_type,
            "timestamp": datetime.now().isoformat()
        })

    patterns = pattern_detector.analyze_operation(operation_type, context)
    assert any(p["type"] == "repetition" for p in patterns)
    assert any(p["action"] == operation_type for p in patterns)

@pytest.mark.asyncio
async def test_timing_pattern_detection(pattern_detector):
    operation_type = "screenshot"

    # Add operations with specific timing
    base_time = datetime.now()
    for i in range(3):
        pattern_detector.patterns.append({
            "action": operation_type,
            "timestamp": (base_time + timedelta(seconds=i*0.5)).isoformat()
        })

    patterns = pattern_detector.analyze_operation(operation_type, {})
    timing_patterns = [p for p in patterns if p["type"] == "timing"]
    assert timing_patterns
    assert timing_patterns[0]["pattern"]["type"] == "rapid_succession"
    assert timing_patterns[0]["pattern"]["average_interval"] < 1.0

@pytest.mark.asyncio
async def test_sequence_detection(pattern_detector):
    # Add a sequence of different operations
    operations = ["click", "type", "screenshot"]
    for op in operations:
        pattern_detector.patterns.append({
            "action": op,
            "timestamp": datetime.now().isoformat()
        })

    patterns = pattern_detector.analyze_operation(operations[-1], {})
    sequence_patterns = [p for p in patterns if p["type"] == "sequence"]
    assert sequence_patterns
    assert len(sequence_patterns[0]["actions"]) >= 2

def test_prometheus_metrics(monitoring):
    # Test tool execution metrics
    monitoring.record_tool_execution("computer", "click", 0.5)
    monitoring.record_tool_execution("computer", "type", 1.0)

    # Test pattern detection metrics
    monitoring.record_pattern_detection("repetition")
    monitoring.record_pattern_detection("sequence")

    # Test error metrics
    monitoring.record_error("computer", "validation_error")

    # Verify metrics were recorded
    assert "tool_execution_duration" in monitoring._metrics
    assert "pattern_detection_total" in monitoring._metrics
    assert "error_total" in monitoring._metrics

def test_time_series_metrics():
    metrics = TimeSeriesMetrics()

    # Record some operations
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=1)

    metrics.record_operation(
        operation_type="click",
        start_time=start_time,
        end_time=end_time,
        metadata={"x": 100, "y": 100}
    )

    latest = metrics.get_latest()
    assert "operation_duration" in latest
    assert latest["operation_duration"]["value"] == pytest.approx(1.0)

def test_meta_cognitive_state():
    state = MetaCognitiveState()

    # Test state updates
    operation1 = {"action": "click", "coordinates": [100, 100]}
    operation2 = {"action": "type", "text": "test"}

    state.update(operation1)
    assert state.current["action"] == "click"
    assert len(state.history) == 1

    state.update(operation2)
    assert state.current["action"] == "type"
    assert len(state.history) == 2

@pytest.mark.asyncio
async def test_monitoring_integration():
    with patch('prometheus_client.start_http_server'):
        integration = MonitoringIntegration()

        # Test tool metrics recording
        metrics_data = {
            "operation_duration": {
                "value": 1.0,
                "operation": "click"
            },
            "resource_usage": {
                "cpu": 50.0,
                "memory": 1024.0
            }
        }

        integration.record_tool_metrics("computer", metrics_data)

        # Test pattern metrics recording
        patterns = [
            {"type": "repetition", "count": 3},
            {"type": "sequence", "actions": ["click", "type"]}
        ]

        integration.record_pattern_metrics(patterns)

        # Test error recording
        integration.record_error("computer", "test error")
