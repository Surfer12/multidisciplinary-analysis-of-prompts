# Computer Use Analysis Framework

A comprehensive framework for analyzing and understanding computer interactions in AI systems, with a focus on:
- System resource utilization
- Tool usage patterns
- Security and isolation
- Development environment optimization

## Project Structure

```
.
├── src/
│   └── python/
│       └── computer_use/      # Core analysis package
│           ├── analysis/      # Analysis tools
│           ├── models/        # Data models
│           └── visualization/ # Visualization tools
├── notebooks/                 # Analysis notebooks
├── data/
│   ├── raw/                  # Raw interaction data
│   └── processed/            # Processed analysis results
└── monitoring/               # System monitoring
```

## Quick Start

1. Start the analysis environment:
```bash
docker compose up computer-use-analysis
```

2. Access the tools:
- Analysis Dashboard: http://localhost:8501
- Jupyter Lab: http://localhost:8888
- Monitoring: http://localhost:3000

## Development

For development work:
```bash
docker compose up analysis-dev
```

## Testing

Run the test suite:
```bash
docker compose up analysis-test
```

## Documentation

Detailed documentation is available in the `docs/` directory.

## License

[License details]
