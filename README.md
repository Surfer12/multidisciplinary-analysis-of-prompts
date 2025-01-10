# Analysis of Prompts

A comprehensive toolkit for analyzing and enhancing AI prompts, featuring visualization tools, Anthropic API integration, and automated testing capabilities.

## Features

### 1. Visualization Components
- Interactive dashboards for data visualization
- Pattern analysis and visualization tools
- Performance metrics visualization
- Network graph visualization for concept relationships

### 2. Anthropic Integration
- Direct integration with Anthropic's API
- Code analysis and improvement suggestions
- Documentation enhancement
- Advanced prompt generation and analysis

### 3. Development Tools
- Automated code quality checks
- Comprehensive testing framework
- Performance profiling tools
- Documentation generation

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/analysis-of-prompts.git
   cd analysis-of-prompts
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Usage

### Running the Visualization Dashboard
```bash
streamlit run src/visualization/dashboard.py
```

### Using the Anthropic Tool
```python
from src.tools.anthropic_tool import AnthropicTool

# Initialize the tool
tool = AnthropicTool()

# Analyze code
result = tool.analyze_code(code_snippet)

# Enhance documentation
documented_code = tool.enhance_documentation(code_snippet)

# Get improvement suggestions
suggestions = tool.suggest_improvements(code_snippet)
```

### Running Tests
```bash
pytest
```

## Project Structure

```
analysis-of-prompts/
├── src/
│   ├── visualization/
│   │   ├── pattern_viz.py
│   │   └── dashboard.py
│   └── tools/
│       └── anthropic_tool.py
├── tests/
│   ├── test_visualization/
│   │   └── test_pattern_viz.py
│   └── test_tools/
│       └── test_anthropic_tool.py
├── docs/
├── requirements-dev.txt
├── setup.py
├── .pre-commit-config.yaml
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality:
   ```bash
   pytest
   pre-commit run --all-files
   ```
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
