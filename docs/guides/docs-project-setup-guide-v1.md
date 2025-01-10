# Project Setup Guide

This guide will walk you through setting up the Analysis of Prompts project environment.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Git
- Mojo SDK (optional, for Mojo development)

## Installation Steps

1. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd analysis-of-prompts
   ```

2. **Set Up Python Environment**
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r config/requirements.txt
   ```

3. **Docker Setup**
   ```bash
   # Build and start containers
   docker-compose -f config/docker-compose.yml up -d
   ```

4. **Configure Development Environment**
   - Copy example configuration files:
     ```bash
     cp config/cursorrules/config-file-renaming-rules.cursorrules.example config/cursorrules/config-file-renaming-rules.cursorrules
     ```
   - Update configuration files with your settings

## Project Structure

The project follows a structured organization:

- `src/`: Source code
  - `mojo/`: Mojo language source files
  - `python/`: Python source files
- `config/`: Configuration files
- `data/`: Data files
- `docs/`: Documentation
- `utils/`: Utility scripts
- `tests/`: Test suites

## Development Workflow

1. **Create a New Feature**
   - Create a new branch
   - Follow naming conventions from README.md
   - Implement changes
   - Add tests

2. **Running Tests**
   ```bash
   # Run Python tests
   pytest tests/

   # Run Mojo tests (if applicable)
   mojo test src/mojo/tests/
   ```

3. **Code Style**
   - Follow PEP 8 for Python code
   - Use provided .cursorrules for consistent formatting

## Troubleshooting

Common issues and their solutions:

1. **Dependency Issues**
   - Ensure virtual environment is activated
   - Update pip: `pip install --upgrade pip`
   - Check Python version compatibility

2. **Docker Issues**
   - Verify Docker daemon is running
   - Check port conflicts
   - Review logs: `docker-compose logs`

## Additional Resources

- Project Documentation: `docs/`
- Contributing Guidelines: `docs/docs-security-guidelines.md`
- Example Code: `examples/`
