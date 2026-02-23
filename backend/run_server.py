#!/usr/bin/env python3
"""
GPT-Researcher Backend Server Startup Script

Run this to start the research API server.
"""

import uvicorn
import os
import sys
import argparse

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start GPT-Researcher server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    args = parser.parse_args()

    # Change to backend directory
    os.chdir(backend_dir)

    # Start the server
    uvicorn.run(
        "server.app:app",
        host=args.host,
        port=args.port,
        reload=True,
        log_level="info"
    )



