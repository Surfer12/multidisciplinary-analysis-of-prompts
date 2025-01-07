# Claude Computer Use Demo with Meta-Cognitive Tools

This repository contains an enhanced version of the Anthropic Computer Use Demo, integrated with meta-cognitive tools for pattern recognition, adaptation, and performance monitoring.

## Features

- **Meta-Cognitive Capabilities**
  - Pattern recognition in tool execution
  - Adaptive behavior based on resource usage
  - Performance monitoring and metrics
  - State tracking and analysis

- **Enhanced UI**
  - Real-time visualization of patterns
  - Performance metrics dashboard
  - Tool execution history
  - Adaptation insights

## Prerequisites

- Docker and Docker Compose
- Anthropic API key
- (Optional) AWS credentials for Bedrock
- (Optional) Google Cloud credentials for Vertex AI

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/computer-use-demo.git
cd computer-use-demo
```

2. Set up environment variables:
```bash
# Create .env file
cat > .env << EOL
ANTHROPIC_API_KEY=your_api_key_here
CLOUD_ML_REGION=your_region  # Optional, for Google Cloud
EOL
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

4. Access the application:
- Web Interface: http://localhost:8501
- VNC (for debugging): localhost:5900

## Configuration

### API Providers

The demo supports multiple API providers:
- Anthropic (default)
- AWS Bedrock
- Google Vertex AI

Configure the provider in the web interface under Settings.

### Meta-Cognitive Settings

Adjust meta-cognitive behavior in the UI:
- Pattern analysis sensitivity
- Adaptation thresholds
- Performance monitoring intervals

## Development

### Project Structure

```
.
├── computer_use_demo/     # Core demo code
├── cognitive_framework/   # Meta-cognitive framework
├── examples/             # Example workflows
├── docs/                # Documentation
├── scripts/             # Startup scripts
└── config/              # Configuration files
```

### Running Tests

```bash
# Inside the container
pytest packages/core/tests/
```

### Adding New Features

1. Extend meta-cognitive capabilities:
   - Add new pattern types in `MetaComputerTool`
   - Implement new observers
   - Enhance the visitor system

2. Improve visualization:
   - Add new metrics
   - Create custom charts
   - Enhance the UI

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Check API key configuration
   - Verify network connectivity
   - Ensure correct provider settings

2. **Display Issues**
   - Restart the container
   - Check Xvfb logs
   - Verify VNC connection

3. **Performance Problems**
   - Adjust resource limits in docker-compose.yml
   - Monitor container metrics
   - Check adaptation thresholds

### Debugging

1. Access container logs:
```bash
docker-compose logs -f
```

2. Connect via VNC:
```bash
# Use any VNC viewer
vncviewer localhost:5900
```

3. Access shell:
```bash
docker-compose exec computer-use-demo bash
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details
