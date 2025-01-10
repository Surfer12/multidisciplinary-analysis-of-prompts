# Use the template and override specific values
ARG BASE_IMAGE=ubuntu:22.04
FROM ${BASE_IMAGE} AS base

# --- Builder Stage ---
FROM base AS builder

# Set up working directory
WORKDIR /app

# Copy dependency files
COPY config/requirements.txt .

# Install dependencies into a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
  pip install --no-cache-dir \
  anthropic pytest streamlit jupyter notebook

# --- Development Stage ---
FROM builder AS dev

# Create a non-root user
RUN useradd -m -s /bin/bash appuser
USER appuser
WORKDIR /home/appuser

# Set up Python environment
ENV PYTHONPATH=/home/appuser/app/src/python \
  MOJO_PATH=/home/appuser/app/src/mojo \
  PATH="/home/appuser/.local/bin:${PATH}"

# Copy project files
COPY --chown=appuser:appuser . /home/appuser/app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /home/appuser/venv

# Expose ports
EXPOSE 8501 8888 5678

# Create development tools script
COPY <<EOF /home/appuser/dev.sh
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

RUN chmod +x /home/appuser/dev.sh

# Set up Jupyter configuration (if needed)
RUN jupyter notebook --generate-config && \
  echo "c.NotebookApp.token = ''" >> /home/appuser/.jupyter/jupyter_notebook_config.py && \
  echo "c.NotebookApp.password = ''" >> /home/appuser/.jupyter/jupyter_notebook_config.py && \
  echo "c.NotebookApp.ip = '0.0.0.0'" >> /home/appuser/.jupyter/jupyter_notebook_config.py

# --- Production Stage ---
FROM python:3.11-slim AS prod

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y \
  curl \
  vim \
  wget \
  htop \
  tmux \
  graphviz \
  postgresql-client \
  redis-tools \
  git \
  && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set up working directory
WORKDIR /app

# Copy necessary files
COPY src /app/src
COPY docs /app/docs
COPY examples /app/examples
COPY tests /app/tests

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

# Default command
CMD ["python", "-m", "pytest", "tests/python/meta_cognitive/test_pattern_recognition.py", "tests/python/meta_cognitive/test_pattern_visualization.py", "-v"]
