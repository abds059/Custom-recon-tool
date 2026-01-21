# Use slim Python image
FROM python:3.12-slim

# Disable Python buffering (better logs)
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency files first (Docker cache optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Create output directories inside container
RUN mkdir -p output/raw output/reports

# Default entrypoint
ENTRYPOINT ["python", "main.py"]
