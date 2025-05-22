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
EXPOSE 8000

# Run the application with core installation
CMD bash -c "./install_core.sh && uvicorn sahur_server.main:app --host 0.0.0.0 --port 8000"
