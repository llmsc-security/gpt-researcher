#!/bin/bash
# GPT-Researcher Docker Build and Run Script
# This script builds the Docker image and runs the container with port mapping

set -e

# Configuration
IMAGE_NAME="gpt-researcher:latest"
CONTAINER_NAME="gpt-researcher"
HOST_PORT=11250
CONTAINER_PORT=8000

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "GPT-Researcher Docker Build and Run"
echo "=========================================="
echo "Repository: ${SCRIPT_DIR}"
echo "Image: ${IMAGE_NAME}"
echo "Container: ${CONTAINER_NAME}"
echo "Host Port: ${HOST_PORT}"
echo "Container Port: ${CONTAINER_PORT}"
echo "=========================================="

# Build the Docker image
echo ""
echo "Building Docker image..."
docker build -t "${IMAGE_NAME}" "${SCRIPT_DIR}"

# Run the Docker container
echo ""
echo "Starting container..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    -p "${HOST_PORT}:${CONTAINER_PORT}" \
    --env-file "${SCRIPT_DIR}/.env" \
    -v "${SCRIPT_DIR}/my-docs:/app/my-docs:rw" \
    -v "${SCRIPT_DIR}/outputs:/app/outputs:rw" \
    --restart always \
    "${IMAGE_NAME}"

echo ""
echo "=========================================="
echo "Container started successfully!"
echo "=========================================="
echo "Server is accessible at: http://localhost:${HOST_PORT}"
echo ""
echo "View container logs: docker logs -f ${CONTAINER_NAME}"
echo "Stop container: docker stop ${CONTAINER_NAME}"
echo "Remove container: docker rm ${CONTAINER_NAME}"
echo "=========================================="
