FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    xterm \
    firefox-esr \
    tint2 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the cognitive framework and computer use demo
COPY packages/core/cognitive_framework /app/cognitive_framework
COPY references/anthropic-quickstarts/computer-use-demo/computer_use_demo /app/computer_use_demo

# Copy example workflows and documentation
COPY examples /app/examples
COPY docs /app/docs

# Set up virtual display
ENV DISPLAY=:1

# Copy startup scripts
COPY scripts/start_all.sh /app/
COPY scripts/start_xvfb.sh /app/
RUN chmod +x /app/start_all.sh /app/start_xvfb.sh

# Create necessary directories
RUN mkdir -p /app/.config/tint2

# Copy tint2 configuration
COPY config/tint2rc /app/.config/tint2/tint2rc

# Set up environment variables
ENV PYTHONPATH=/app
ENV ANTHROPIC_API_KEY=""
ENV CLOUD_ML_REGION=""

# Expose Streamlit port
EXPOSE 8501

# Start the application
CMD ["./start_all.sh"]
