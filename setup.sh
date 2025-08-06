#!/bin/bash

# Computer Vision Project Setup Script
echo "🚀 Setting up Computer Vision project..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   - Mac: https://docs.docker.com/desktop/install/mac-install/"
    echo "   - Windows: https://docs.docker.com/desktop/install/windows-install/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p data models logs

# Build Docker image
echo "🔨 Building Docker image..."
docker-compose build

echo "✅ Setup complete!"
echo ""
echo "📋 Available commands:"
echo "   Start development environment: docker-compose up"
echo "   Start with Jupyter Lab:       docker-compose --profile jupyter up"
echo "   Run interactive shell:        docker-compose run --rm cv-app bash"
echo ""
echo "🌐 Accessible URLs:"
echo "   Main app: http://localhost:8000"
echo "   Jupyter:  http://localhost:8888 (when using jupyter profile)"