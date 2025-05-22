FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Make the install_core.sh script executable
RUN chmod +x install_core.sh

# Run the application with core installation
ENTRYPOINT ["/bin/bash", "-c", "./install_core.sh && python -m sahur_batch.main"]
