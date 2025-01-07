import asyncio
from typing import Dict, List
from anthropic import Anthropic
from cognitive_framework.tools import CognitiveToolCollection
from cognitive_framework.models import (
    Concept,
    StageAnalysisItem,
    EmergentFramework
)

async def main():
    # Initialize Anthropic client
    client = Anthropic(api_key="your-api-key")

    # Create tool collection
    mojo_type_registry = {
        "Concept": Concept,
        "StageAnalysisItem": StageAnalysisItem,
        "EmergentFramework": EmergentFramework
    }

    analysis_config = {
        "pattern_analysis": {
            "min_pattern_frequency": 2,
            "max_pattern_depth": 3
        },
        "trend_analysis": {
            "window_size": 5,
            "min_trend_strength": 0.7
        }
    }

    tools = CognitiveToolCollection.create_default_collection(
        mojo_type_registry=mojo_type_registry,
        analysis_config=analysis_config
    )

    # Example: Create a concept using the Mojo structure tool
    concept_data = {
        "id": 1,
        "name": "Fluid Learning Paradigm",
        "relevant_input_excerpt": "...emphasizing conceptual exploration and flexible thinking..."
    }

    result = tools.execute_tool(
        "mojo_structure",
        operation="create",
        structure_type="Concept",
        data=concept_data
    )

    if result.success:
        print("Created concept:", result.data)
    else:
        print("Error creating concept:", result.error)

    # Example: Analyze patterns using the meta-analysis tool
    analysis_data = [
        {
            "type": "concept",
            "data": concept_data,
            "timestamp": "2024-01-15T10:00:00Z"
        },
        # Add more data points for analysis
    ]

    result = tools.execute_tool(
        "meta_analysis",
        operation="pattern_analysis",
        data=analysis_data,
        analysis_type="structural"
    )

    if result.success:
        print("Pattern analysis result:", result.data)
    else:
        print("Error in pattern analysis:", result.error)

    # Example: Use tools with Claude
    messages = [
        {
            "role": "user",
            "content": "Analyze this concept and suggest improvements."
        }
    ]

    response = await client.messages.create(
        model="claude-3-opus-20240229",
        messages=messages,
        tools=tools.to_anthropic_params(),
        max_tokens=1000
    )

    print("Claude's response:", response.content)

    # Example: Process Claude's tool calls
    for tool_call in response.tool_calls:
        result = tools.execute_tool(
            tool_call.name,
            **tool_call.parameters
        )

        print(f"Tool '{tool_call.name}' result:", result.data if result.success else result.error)

    # Example: Review tool execution history
    history = tools.get_tool_history()
    print("\nTool execution history:")
    for entry in history:
        print(f"- {entry['tool']}: {'Success' if entry['success'] else 'Failed'}")
        if not entry['success']:
            print(f"  Error: {entry['error']}")

if __name__ == "__main__":
    asyncio.run(main())
