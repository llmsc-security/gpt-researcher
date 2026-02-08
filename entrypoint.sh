#!/bin/bash
# GPT-Researcher Entrypoint Script
# This script starts the FastAPI server with the specified configuration

set -e

echo "Starting GPT-Researcher server..."

# Change to /app where gpt_researcher module is located
cd /app

# Execute the command passed to the container
# Default: run the server with python3 backend/run_server.py
exec python3 backend/run_server.py --host 0.0.0.0 --port 11250 "$@"
