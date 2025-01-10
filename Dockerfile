FROM python:3.11-slim

# Install system build dependencies with retries
RUN apt-get update && apt-get install -y --retries 5 --retry-delay 5 \
    git \
    build-essential \
    python3-dev \
    curl \
    vim \
    wget \
    htop \
    tmux \
    graphviz \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy only dependency files first to leverage caching
COPY config/requirements.txt .
COPY config/pixi.toml .
COPY .pre-commit-config.yaml .

# Install dependencies into a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies all at once to reduce layers
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
    anthropic pytest pytest-watch black flake8 mypy jupyter notebook ipykernel \
    matplotlib seaborn numpy pandas scikit-learn streamlit watchdog psutil \
    dask[complete] apache-airflow slackclient plotly dash bokeh altair networkx \
    graphviz pydot pre-commit hypothesis pytest-asyncio pytest-mock pytest-profiling \
    memory_profiler line_profiler snakeviz py-spy debugpy pytest-cov pytest-xdist \
    pytest-timeout pytest-randomly pytest-repeat pytest-benchmark ipdb rich tqdm \
    jupyterlab jupyter-dash jupyter-server-proxy nbconvert nbformat nbdime jupytext \
    papermill

# Set up pre-commit hooks
RUN git init && pre-commit install

# Copy source code and other necessary files
COPY src /app/src
COPY docs /app/docs
COPY examples /app/examples
COPY tests /app/tests
COPY config /app/config  # Copy the config directory

# Set up environment variables
ENV PYTHONPATH=/app/src/python \
    MOJO_PATH=/app/src/mojo \
    ANTHROPIC_API_KEY="x-api-key" \
    PYTHONBREAKPOINT=ipdb.set_trace \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    JUPYTER_ENABLE_LAB=yes \
    MPLBACKEND=Agg

# Create data directories
RUN mkdir -p /app/data/raw /app/data/processed

# Set up Jupyter configuration
RUN jupyter notebook --generate-config && \
    echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py

# Create development tools script
COPY <<EOF /app/dev.sh
#!/bin/bash
case "\$1" in
  "test")
    pytest tests/python/meta_cognitive -v \$2
    ;;
  "watch")
    ptw tests/python/meta_cognitive --now
    ;;
  "lint")
    pre-commit run --all-files
    ;;
  "profile")
    case "\$2" in
      "memory")
        mprof run \$3
        mprof plot
        ;;
      "cpu")
        py-spy record -o profile.svg -- python \$3
        ;;
      "line")
        kernprof -l -v \$3
        ;;
      *)
        echo "Usage: ./dev.sh profile [memory|cpu|line] <script>"
        ;;
    esac
    ;;
  "notebook")
    jupyter lab --allow-root --no-browser --port=8888
    ;;
  "streamlit")
    streamlit run src/python/meta_cognitive_tools/visualization/app.py
    ;;
  "dash")
    python src/python/meta_cognitive_tools/visualization/dashboard.py
    ;;
  "debug")
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client \$2
    ;;
  *)
    echo "Usage: ./dev.sh [test|watch|lint|profile|notebook|streamlit|dash|debug] [additional args]"
    ;;
esac
EOF

RUN chmod +x /app/dev.sh

# Expose ports
EXPOSE 8501 8888 5678

# Default command
CMD ["python", "-m", "pytest", "tests/python/meta_cognitive/test_pattern_recognition.py", "tests/python/meta_cognitive/test_pattern_visualization.py", "-v"]
