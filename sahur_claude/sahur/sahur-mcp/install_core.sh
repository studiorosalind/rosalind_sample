#!/bin/bash
# Script to install sahur-core in the Docker container

# Check if sahur-core directory exists
if [ -d "/app/sahur-core" ]; then
    echo "Installing sahur-core..."
    pip install -e /app/sahur-core
    echo "sahur-core installed successfully."
else
    echo "Error: sahur-core directory not found."
    exit 1
fi
