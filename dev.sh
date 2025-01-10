#!/bin/bash

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment variables
if [ -f "$PROJECT_ROOT/.env" ]; then
    # Use awk to filter out comments and empty lines, then export
    export $(awk '!/^#/ && NF' "$PROJECT_ROOT/.env" | xargs)
fi

# Function to display usage
usage() {
    echo "Usage: $0 [mode]"
    echo ""
    echo "Modes:"
    echo "  notebook   - Launch Jupyter Lab"
    echo "  streamlit  - Run Streamlit application"
    echo "  test       - Run pytest in Docker"
    echo "  local-test - Run pytest locally without Docker"
    echo "  build      - Build Docker image"
    echo "  dev        - Start development environment"
    echo "  help       - Show this help message"
}

# Activate virtual environment
activate_venv() {
    if [ -d "$PROJECT_ROOT/venv" ]; then
        source "$PROJECT_ROOT/venv/bin/activate"
    elif [ -d "$PROJECT_ROOT/.venv" ]; then
        source "$PROJECT_ROOT/.venv/bin/activate"
    else
        echo "No virtual environment found. Please create one using 'python3 -m venv venv'"
        exit 1
    fi
}

# Build Docker image
build_image() {
    echo "Building Docker image..."
    docker build -t analysis-of-prompts:dev "$PROJECT_ROOT"
}

# Local test without Docker
local_test() {
    # Activate virtual environment
    activate_venv

    # Install dependencies
    pip install -r "$PROJECT_ROOT/requirements.txt"
    pip install -r "$PROJECT_ROOT/requirements-dev.txt"

    # Run tests
    cd "$PROJECT_ROOT"
    PYTHONPATH=. pytest tests -v

    # Deactivate virtual environment
    deactivate
}

# Launch Jupyter Notebook
launch_notebook() {
    build_image
    docker run \
        -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
        -v "$PROJECT_ROOT":/home/appuser/app \
        -v "$HOME/.anthropic":/home/appuser/.anthropic \
        -p 8888:8888 \
        -p 8501:8501 \
        -p 5678:5678 \
        -it analysis-of-prompts:dev \
        jupyter lab --allow-root --no-browser --port=8888
}

# Launch Streamlit
launch_streamlit() {
    build_image
    docker run \
        -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
        -v "$PROJECT_ROOT":/home/appuser/app \
        -v "$HOME/.anthropic":/home/appuser/.anthropic \
        -p 8501:8501 \
        -p 8888:8888 \
        -p 5678:5678 \
        -it analysis-of-prompts:dev \
        streamlit run src/app.py
}

# Run Tests in Docker
run_tests() {
    build_image
    docker run \
        -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
        -v "$PROJECT_ROOT":/home/appuser/app \
        -v "$HOME/.anthropic":/home/appuser/.anthropic \
        -it analysis-of-prompts:dev \
        pytest tests -v
}

# Development environment
dev_environment() {
    build_image
    docker run \
        -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
        -v "$PROJECT_ROOT":/home/appuser/app \
        -v "$HOME/.anthropic":/home/appuser/.anthropic \
        -p 8501:8501 \
        -p 8888:8888 \
        -p 5678:5678 \
        -it analysis-of-prompts:dev \
        /bin/bash
}

# Main script logic
case "$1" in
    notebook)
        launch_notebook
        ;;
    streamlit)
        launch_streamlit
        ;;
    test)
        run_tests
        ;;
    local-test)
        local_test
        ;;
    build)
        build_image
        ;;
    dev)
        dev_environment
        ;;
    help|*)
        usage
        ;;
esac
