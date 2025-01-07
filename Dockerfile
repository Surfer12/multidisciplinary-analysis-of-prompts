# Multi-stage build for development environment
FROM python:3.9-slim as python-base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
WORKDIR /app
COPY packages/core/requirements/*.txt ./requirements/
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements/dev.txt

# Set up TypeScript environment
COPY packages/typescript/package*.json ./
RUN npm install

# Set up Mojo environment
# Add Mojo installation steps here

# Development stage
FROM python-base as dev
WORKDIR /app
COPY . .

# Install development dependencies
RUN cd packages/core && pip install -e ".[dev]"
RUN cd packages/typescript && npm install

# Set up development environment
ENV PYTHONPATH=/app/packages/core/src
ENV NODE_PATH=/app/packages/typescript/node_modules

CMD ["bash"]
