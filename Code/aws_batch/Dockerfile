# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy job code and data contract
COPY batch_job.py .
COPY data_contract.json .

# Copy requirements file
COPY requirements.txt .

# Install system dependencies for FTP and AWS SDK
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        unzip \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the batch job
ENTRYPOINT ["python", "batch_job.py"]
