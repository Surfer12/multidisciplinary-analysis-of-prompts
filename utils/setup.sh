#!/bin/bash

# Setup script for development environment

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "🚀 Setting up development environment..."

# Python/Core setup
echo "📦 Setting up Core package..."
cd packages/core
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cd ../..

# TypeScript setup
echo "🌐 Setting up TypeScript package..."
cd packages/typescript
npm install
cd ../..

# Mojo setup
echo "🔥 Setting up Mojo package..."
cd packages/mojo
# Add Mojo-specific setup here
cd ../..

# Install git hooks
echo "🔨 Setting up git hooks..."
cp tools/scripts/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

echo -e "${GREEN}✅ Development environment setup complete!${NC}"
