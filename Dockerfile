# Use Ubuntu as base for more flexibility
FROM ubuntu:22.04 AS base

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  git \
  python3 \
  python3-pip \
  python3-venv \
  && rm -rf /var/lib/apt/lists/*

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

# --- Builder Stage ---
FROM base AS builder

# Install dependencies
RUN python3 -m venv /home/appuser/venv && \
  . /home/appuser/venv/bin/activate && \
  pip install --no-cache-dir -r /home/appuser/app/config/requirements.txt && \
  pip install --no-cache-dir \
  anthropic pytest streamlit jupyter notebook

# --- Development Stage ---
FROM base AS dev

# Copy the virtual environment from the builder stage
COPY --from=builder /home/appuser/venv /home/appuser/venv

# Expose ports
EXPOSE 8501 8888 5678

# Create entrypoint script
RUN echo '#!/bin/bash\n\
  if [ "$1" = "test" ]; then\n\
  pytest tests/python/meta_cognitive\n\
  elif [ "$1" = "notebook" ]; then\n\
  jupyter lab --ip 0.0.0.0 --no-browser --allow-root\n\
  elif [ "$1" = "streamlit" ]; then\n\
  streamlit run src/python/meta_cognitive_tools/visualization/app.py\n\
  else\n\
  "$@"\n\
  fi' > /home/appuser/entrypoint.sh && \
  chmod +x /home/appuser/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/home/appuser/entrypoint.sh"]
CMD ["python3"]

# --- Production Stage (Optional) ---
# FROM base AS prod
# ... (Add steps to copy only necessary files and configure for production)
