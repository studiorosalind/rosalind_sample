FROM python:3.9-slim

WORKDIR /app

# Copy sahur-core first
COPY ../sahur-core /app/sahur-core

# Install sahur-core
RUN pip install -e /app/sahur-core

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Expose the port
EXPOSE 8002

# Run the application
CMD ["python", "-m", "sahur_mcp.main"]
