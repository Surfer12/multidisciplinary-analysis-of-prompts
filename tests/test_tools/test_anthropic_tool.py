"""Tests for the Anthropic tool integration."""
from unittest.mock import MagicMock, patch

import pytest

from src.tools.anthropic_tool import AnthropicTool


@pytest.fixture
def mock_anthropic_client():
    """Create a mock Anthropic client."""
    with patch("anthropic.Client") as mock_client:
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="Test response")]
        mock_client.return_value.messages.create.return_value = mock_message
        yield mock_client


@pytest.fixture
def anthropic_tool(mock_anthropic_client):
    """Create an AnthropicTool instance with mocked client."""
    with patch("os.getenv", return_value="dummy_key"):
        return AnthropicTool()


def test_generate_response(anthropic_tool):
    """Test generating a response."""
    response = anthropic_tool.generate_response("Test prompt")
    assert response == "Test response"

    # Test with system prompt
    response = anthropic_tool.generate_response(
        "Test prompt", system_prompt="System instruction"
    )
    assert response == "Test response"


def test_analyze_code(anthropic_tool):
    """Test code analysis."""
    code = """
    def example():
        print("Hello, World!")
    """
    result = anthropic_tool.analyze_code(code)
    assert result["success"] is True
    assert result["analysis_type"] == "general"
    assert isinstance(result["response"], str)

    # Test with context
    context = {"file_type": "python", "purpose": "testing"}
    result = anthropic_tool.analyze_code(code, context=context)
    assert result["success"] is True


def test_enhance_documentation(anthropic_tool):
    """Test documentation enhancement."""
    code = """
    def example():
        print("Hello, World!")
    """
    result = anthropic_tool.enhance_documentation(code)
    assert isinstance(result, str)
    assert len(result) > 0

    # Test with different doc style
    result = anthropic_tool.enhance_documentation(code, doc_style="numpy")
    assert isinstance(result, str)


def test_suggest_improvements(anthropic_tool):
    """Test code improvement suggestions."""
    code = """
    def example():
        print("Hello, World!")
    """
    suggestions = anthropic_tool.suggest_improvements(code)
    assert isinstance(suggestions, list)

    # Test with focus areas
    focus_areas = ["performance", "security"]
    suggestions = anthropic_tool.suggest_improvements(code, focus_areas=focus_areas)
    assert isinstance(suggestions, list)


def test_error_handling(anthropic_tool, mock_anthropic_client):
    """Test error handling in the tool."""
    # Simulate API error
    mock_anthropic_client.return_value.messages.create.side_effect = Exception(
        "API Error"
    )

    # Test error handling in generate_response
    response = anthropic_tool.generate_response("Test prompt")
    assert response == ""

    # Test error handling in analyze_code
    result = anthropic_tool.analyze_code("Test code")
    assert result["success"] is False
    assert "error" in result

    # Test error handling in enhance_documentation
    result = anthropic_tool.enhance_documentation("Test code")
    assert result == "Test code"  # Should return original code on error

    # Test error handling in suggest_improvements
    suggestions = anthropic_tool.suggest_improvements("Test code")
    assert len(suggestions) == 0
