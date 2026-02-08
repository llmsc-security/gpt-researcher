# Multi-stage Dockerfile for GPT-Researcher
# Stage 1: Build stage with Python 3.11-slim
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy the rest of the application
COPY . .

# Set working directory to /app where gpt_researcher module is located
WORKDIR /app

# Expose the port the app will run on (container port 11250)
EXPOSE 11250

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Use the run_server.py entry point with custom port
CMD ["python3", "backend/run_server.py", "--host", "0.0.0.0", "--port", "11250"]
