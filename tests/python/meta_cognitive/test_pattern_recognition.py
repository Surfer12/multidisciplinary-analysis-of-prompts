"""Test module for advanced pattern recognition capabilities in meta-cognitive systems."""

import pytest
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum, auto
import numpy as np
from collections import defaultdict

class PatternType(Enum):
    """Types of patterns that can be recognized."""
    SEQUENTIAL = auto()
    RECURSIVE = auto()
    EMERGENT = auto()
    ADAPTIVE = auto()
    META = auto()

@dataclass
class PatternInstance:
    """Class representing a recognized pattern instance."""
    pattern_type: PatternType
    confidence: float
    context: Dict[str, Any]
    sub_patterns: List['PatternInstance'] = field(default_factory=list)
    meta_data: Dict[str, Any] = field(default_factory=dict)

class AdvancedPatternRecognizer:
    """Advanced pattern recognition system with meta-cognitive capabilities."""

    def __init__(self):
        self.pattern_history: List[PatternInstance] = []
        self.pattern_frequencies: Dict[PatternType, int] = defaultdict(int)
        self.confidence_thresholds: Dict[PatternType, float] = {
            PatternType.SEQUENTIAL: 0.7,
            PatternType.RECURSIVE: 0.8,
            PatternType.EMERGENT: 0.6,
            PatternType.ADAPTIVE: 0.75,
            PatternType.META: 0.85
        }

    def recognize_pattern(self, data: Any, context: Dict[str, Any]) -> Optional[PatternInstance]:
        """Recognize patterns in the given data."""
        # Analyze data for different pattern types
        pattern_scores = self._calculate_pattern_scores(data, context)

        # Find the most confident pattern
        best_pattern = max(pattern_scores.items(), key=lambda x: x[1])
        pattern_type, confidence = best_pattern

        if confidence >= self.confidence_thresholds[pattern_type]:
            pattern = PatternInstance(
                pattern_type=pattern_type,
                confidence=confidence,
                context=context
            )

            # Look for sub-patterns
            sub_patterns = self._identify_sub_patterns(data, context)
            if sub_patterns:
                pattern.sub_patterns.extend(sub_patterns)

            # Record pattern
            self.pattern_history.append(pattern)
            self.pattern_frequencies[pattern_type] += 1

            return pattern
        return None

    def _calculate_pattern_scores(self, data: Any, context: Dict[str, Any]) -> Dict[PatternType, float]:
        """Calculate confidence scores for each pattern type."""
        scores = {}

        # Sequential pattern detection
        scores[PatternType.SEQUENTIAL] = self._detect_sequential_patterns(data)

        # Recursive pattern detection
        scores[PatternType.RECURSIVE] = self._detect_recursive_patterns(data)

        # Emergent pattern detection
        scores[PatternType.EMERGENT] = self._detect_emergent_patterns(data, context)

        # Adaptive pattern detection
        scores[PatternType.ADAPTIVE] = self._detect_adaptive_patterns(data, context)

        # Meta pattern detection
        scores[PatternType.META] = self._detect_meta_patterns(data, context)

        return scores

    def _detect_sequential_patterns(self, data: Any) -> float:
        """Detect sequential patterns in data."""
        # Simplified implementation for testing
        return np.random.uniform(0.6, 0.9)

    def _detect_recursive_patterns(self, data: Any) -> float:
        """Detect recursive patterns in data."""
        # Simplified implementation for testing
        return np.random.uniform(0.7, 0.95)

    def _detect_emergent_patterns(self, data: Any, context: Dict[str, Any]) -> float:
        """Detect emergent patterns in data."""
        # Simplified implementation for testing
        return np.random.uniform(0.5, 0.8)

    def _detect_adaptive_patterns(self, data: Any, context: Dict[str, Any]) -> float:
        """Detect adaptive patterns in data."""
        # Simplified implementation for testing
        return np.random.uniform(0.6, 0.85)

    def _detect_meta_patterns(self, data: Any, context: Dict[str, Any]) -> float:
        """Detect meta-level patterns in data."""
        # Simplified implementation for testing
        return np.random.uniform(0.7, 1.0)

    def _identify_sub_patterns(self, data: Any, context: Dict[str, Any]) -> List[PatternInstance]:
        """Identify sub-patterns within the main pattern."""
        sub_patterns = []
        # Simplified implementation for testing
        if np.random.random() > 0.5:
            sub_pattern = PatternInstance(
                pattern_type=np.random.choice(list(PatternType)),
                confidence=np.random.uniform(0.6, 0.9),
                context=context
            )
            sub_patterns.append(sub_pattern)
        return sub_patterns

    def analyze_pattern_distribution(self) -> Dict[str, Any]:
        """Analyze the distribution of recognized patterns."""
        total_patterns = sum(self.pattern_frequencies.values())
        distribution = {
            'total_patterns': total_patterns,
            'type_distribution': {
                pattern_type.name: count / total_patterns
                for pattern_type, count in self.pattern_frequencies.items()
            } if total_patterns > 0 else {},
            'confidence_stats': self._calculate_confidence_stats(),
            'sub_pattern_stats': self._calculate_sub_pattern_stats()
        }
        return distribution

    def _calculate_confidence_stats(self) -> Dict[str, float]:
        """Calculate confidence statistics for recognized patterns."""
        if not self.pattern_history:
            return {}

        confidences = [p.confidence for p in self.pattern_history]
        return {
            'mean': float(np.mean(confidences)),
            'std': float(np.std(confidences)),
            'min': float(np.min(confidences)),
            'max': float(np.max(confidences))
        }

    def _calculate_sub_pattern_stats(self) -> Dict[str, Any]:
        """Calculate statistics about sub-patterns."""
        if not self.pattern_history:
            return {}

        sub_pattern_counts = [len(p.sub_patterns) for p in self.pattern_history]
        return {
            'mean_sub_patterns': float(np.mean(sub_pattern_counts)),
            'max_sub_patterns': float(np.max(sub_pattern_counts)),
            'total_sub_patterns': sum(sub_pattern_counts)
        }

@pytest.fixture
def pattern_recognizer():
    """Fixture providing an AdvancedPatternRecognizer instance."""
    return AdvancedPatternRecognizer()

def test_pattern_recognition_basic(pattern_recognizer):
    """Test basic pattern recognition capabilities."""
    # Test data and context
    test_data = "Test pattern data"
    context = {'source': 'test', 'complexity': 0.5}

    # Recognize pattern
    pattern = pattern_recognizer.recognize_pattern(test_data, context)

    # Verify pattern recognition
    assert pattern is not None
    assert isinstance(pattern.pattern_type, PatternType)
    assert 0.0 <= pattern.confidence <= 1.0
    assert pattern.context == context

def test_pattern_distribution_analysis(pattern_recognizer):
    """Test pattern distribution analysis."""
    # Generate multiple patterns
    for _ in range(10):
        pattern_recognizer.recognize_pattern(
            "Test data",
            {'source': 'test', 'iteration': _}
        )

    # Analyze distribution
    distribution = pattern_recognizer.analyze_pattern_distribution()

    # Verify analysis results
    assert distribution['total_patterns'] == 10
    assert all(0.0 <= v <= 1.0 for v in distribution['type_distribution'].values())
    assert all(k in ['mean', 'std', 'min', 'max']
              for k in distribution['confidence_stats'].keys())
    assert all(k in ['mean_sub_patterns', 'max_sub_patterns', 'total_sub_patterns']
              for k in distribution['sub_pattern_stats'].keys())

def test_sub_pattern_recognition(pattern_recognizer):
    """Test recognition of sub-patterns."""
    # Generate pattern with potential sub-patterns
    pattern = pattern_recognizer.recognize_pattern(
        "Complex test data",
        {'source': 'test', 'complexity': 0.8}
    )

    # Verify pattern and sub-patterns
    assert pattern is not None
    assert isinstance(pattern.sub_patterns, list)
    if pattern.sub_patterns:
        sub_pattern = pattern.sub_patterns[0]
        assert isinstance(sub_pattern.pattern_type, PatternType)
        assert 0.0 <= sub_pattern.confidence <= 1.0

def test_confidence_thresholds(pattern_recognizer):
    """Test pattern recognition confidence thresholds."""
    # Test multiple pattern recognitions
    recognized_patterns = []
    for _ in range(20):
        pattern = pattern_recognizer.recognize_pattern(
            "Test data",
            {'source': 'test', 'iteration': _}
        )
        if pattern is not None:
            recognized_patterns.append(pattern)

    # Verify confidence thresholds
    for pattern in recognized_patterns:
        threshold = pattern_recognizer.confidence_thresholds[pattern.pattern_type]
        assert pattern.confidence >= threshold
