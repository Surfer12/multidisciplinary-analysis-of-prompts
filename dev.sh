#!/bin/bash

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment variables
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

# Function to display usage
usage() {
    echo "Usage: $0 [mode]"
    echo ""
    echo "Modes:"
    echo "  notebook   - Launch Jupyter Lab"
    echo "  streamlit  - Run Streamlit application"
    echo "  test       - Run pytest"
    echo "  build      - Build Docker image"
    echo "  dev        - Start development environment"
    echo "  help       - Show this help message"
}

# Build Docker image
build_image() {
    echo "Building Docker image..."
    docker build -t analysis-of-prompts:dev "$PROJECT_ROOT"
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

# Run Tests
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
