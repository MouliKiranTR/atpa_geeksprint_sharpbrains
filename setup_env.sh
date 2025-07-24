#!/bin/bash

# Setup script for the Python project
echo "🔧 Setting up Python environment..."

# Set environment variable to prevent __pycache__ generation
export PYTHONDONTWRITEBYTECODE=1
echo "✅ Set PYTHONDONTWRITEBYTECODE=1"

# Remove any existing __pycache__ directories
echo "🗑️  Cleaning up existing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Remove any .pyc files
echo "🗑️  Cleaning up .pyc files..."
find . -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Environment setup complete!"
echo "💡 To make this permanent, add 'export PYTHONDONTWRITEBYTECODE=1' to your shell profile (.bashrc, .zshrc, etc.)" 