#!/bin/bash

# Set the ANTHROPIC_API_KEY environment variable
export ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY

# Set project root to the analysis-of-prompts-v0.2 directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Add src/python to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/src/python:$PROJECT_ROOT/computer-use-demo:$PYTHONPATH"

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
    echo "  setup      - Set up development environment"
    echo "  test       - Run all tests"
    echo "  test-tools - Run tool-specific tests"
    echo "  docker     - Build and run Docker environment"
    echo "  help       - Show this help message"
}

# Function to set up Python virtual environment
setup_venv() {
    echo "Setting up Python virtual environment..."
    if [ ! -d "$PROJECT_ROOT/.venv" ]; then
        python3 -m venv "$PROJECT_ROOT/.venv"
    fi
    source "$PROJECT_ROOT/.venv/bin/activate"
    # Run setup.sh if it exists
    if [ -f "$PROJECT_ROOT/setup.sh" ]; then
        echo "Running setup.sh..."
        bash "$PROJECT_ROOT/setup.sh"
    fi
    pip install -r "$PROJECT_ROOT/utils/pre-commit"
    pip install -r "$PROJECT_ROOT/requirements-dev.txt"
    pip install -r "$PROJECT_ROOT/requirements.txt"
}

# Function to set up Mojo environment
setup_mojo() {
    echo "Setting up Mojo environment..."
    cd "$PROJECT_ROOT/src/mojo"
    # Add Mojo-specific setup here
}

# Function to run tests
run_tests() {
    local test_path="$1"
    echo "Running tests in $test_path..."

    # Activate virtual environment
    source "$PROJECT_ROOT/.venv/bin/activate"

    # Run pytest with the specified path
    PYTHONPATH="$PROJECT_ROOT/src/python:$PYTHONPATH" pytest "$test_path" -v
}

# Function to build and run Docker
setup_docker() {
    echo "Setting up Docker environment..."
    docker build -t analysis-of-prompts:dev -f "$PROJECT_ROOT/Dockerfile" "$PROJECT_ROOT"

    docker run -it \
        -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
        -v "$PROJECT_ROOT":/app \
        -v "$HOME/.anthropic":/root/.anthropic \
        -p 8888:8888 \
        analysis-of-prompts:dev
}

# Function to run Streamlit interface
run_streamlit() {
    echo "Starting Streamlit interface..."
    source "$PROJECT_ROOT/.venv/bin/activate"
    streamlit run "$PROJECT_ROOT/computer-use-demo/streamlit.py"
}

# Main setup function
setup() {
    setup_venv
    setup_mojo
    echo "Environment setup complete"
}

# Main script logic
case "$1" in
    setup)
        setup
        ;;
    test)
        # Run all tests
        run_tests "$PROJECT_ROOT/tests"
        run_tests "$PROJECT_ROOT/computer-use-demo/tests"
        ;;
    test-tools)
        # Run tool-specific tests
        run_tests "$PROJECT_ROOT/tests/test_tools"
        run_tests "$PROJECT_ROOT/computer-use-demo/tests/tools"
        ;;
    docker)
        setup_docker
        ;;
    streamlit)
        run_streamlit
        ;;
    help|*)
        usage
        ;;
esac
