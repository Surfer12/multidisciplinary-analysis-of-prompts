# Use an ARG for the base image to allow easy customization
ARG BASE_IMAGE=python:3.11-slim
FROM ${BASE_IMAGE} AS base

# --- Builder Stage ---
FROM base AS builder

# Set up working directory
WORKDIR /app

# Copy only dependency files first (for better caching)
COPY requirements.txt .

# Create a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Development Stage ---
FROM builder AS dev

# Create a non-root user
RUN useradd -m -s /bin/bash appuser
USER appuser
WORKDIR /home/appuser

# Set up environment variables
ENV PYTHONPATH=/home/appuser/app/src \
  PATH="/home/appuser/.local/bin:${PATH}"

# Copy project files
COPY --chown=appuser:appuser . /home/appuser/app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /home/appuser/venv

# Expose development ports
EXPOSE 8501 8888 5678

# Create a dev script (optional but recommended)
COPY <<EOF /home/appuser/dev.sh
#!/bin/bash
case "\$1" in
  "test")
    pytest tests -v
    ;;
  "notebook")
    jupyter lab --allow-root --no-browser --port=8888
    ;;
  "streamlit")
    streamlit run src/app.py
    ;;
  *)
    echo "Usage: ./dev.sh [test|notebook|streamlit]"
    ;;
esac
EOF

RUN chmod +x /home/appuser/dev.sh

# --- Production Stage ---
FROM python:3.11-slim AS prod

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
  curl \
  git \
  && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set up working directory
WORKDIR /app

# Copy necessary project files
COPY src /app/src
COPY tests /app/tests

# Set up environment variables
ENV PYTHONPATH=/app/src \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

# Create data directories
RUN mkdir -p /app/data/raw /app/data/processed

# Default command (can be overridden)
CMD ["python", "-m", "pytest", "tests", "-v"]
