FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    python3-dev \
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

# Copy configuration files
COPY config/requirements.txt .
COPY config/pixi.toml .
COPY .pre-commit-config.yaml .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir \
    anthropic \
    pytest \
    pytest-watch \
    black \
    flake8 \
    mypy \
    jupyter \
    notebook \
    ipykernel \
    matplotlib \
    seaborn \
    numpy \
    pandas \
    scikit-learn \
    streamlit \
    watchdog \
    psutil \
    dask[complete] \
    apache-airflow \
    slackclient \
    plotly \
    dash \
    bokeh \
    altair \
    networkx \
    graphviz \
    pydot \
    pre-commit \
    hypothesis \
    pytest-asyncio \
    pytest-mock \
    pytest-profiling \
    memory_profiler \
    line_profiler \
    snakeviz \
    py-spy \
    debugpy

# Install development tools
RUN pip install --no-cache-dir \
    pytest-cov \
    pytest-xdist \
    pytest-timeout \
    pytest-randomly \
    pytest-repeat \
    pytest-benchmark \
    ipdb \
    rich \
    tqdm \
    jupyterlab \
    jupyter-dash \
    jupyter-server-proxy \
    nbconvert \
    nbformat \
    nbdime \
    jupytext \
    papermill

# Set up pre-commit hooks
RUN git init && pre-commit install

# Copy source code
COPY src/python/prompt_analysis_engine /app/src/python/prompt_analysis_engine
COPY src/python/meta_cognitive_tools /app/src/python/meta_cognitive_tools
COPY src/python/pattern_recognition /app/src/python/pattern_recognition
COPY src/python/framework_validation /app/src/python/framework_validation
COPY src/mojo/performance_optimization /app/src/mojo/performance_optimization
COPY src/mojo/pattern_matching /app/src/mojo/pattern_matching

# Copy documentation and examples
COPY docs /app/docs
COPY examples /app/examples

# Copy test files
COPY tests /app/tests

# Set up environment variables
ENV PYTHONPATH=/app/src/python
ENV MOJO_PATH=/app/src/mojo
ENV ANTHROPIC_API_KEY=""
ENV PYTHONBREAKPOINT=ipdb.set_trace
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV JUPYTER_ENABLE_LAB=yes

# Create data directories
RUN mkdir -p /app/data/raw /app/data/processed

# Set up matplotlib backend for non-interactive environments
ENV MPLBACKEND=Agg

# Set up Jupyter configuration
RUN jupyter notebook --generate-config
RUN echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py

# Create a script to run development tools
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

# Expose ports (8501 for Streamlit, 8888 for Jupyter, 5678 for debugpy)
EXPOSE 8501
EXPOSE 8888
EXPOSE 5678

# Default command
CMD ["python", "-m", "pytest", "tests/python/meta_cognitive/test_pattern_recognition.py", "tests/python/meta_cognitive/test_pattern_visualization.py", "-v"]
