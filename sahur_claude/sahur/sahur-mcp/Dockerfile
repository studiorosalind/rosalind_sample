FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Make the install_core.sh script executable
RUN chmod +x install_core.sh

# Expose the port
EXPOSE 8002

# Run the script to install sahur-core and then start the application
CMD ["bash", "-c", "./install_core.sh && python -m sahur_mcp.main"]
