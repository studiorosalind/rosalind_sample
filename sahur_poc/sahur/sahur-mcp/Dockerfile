FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY sahur_mcp/ ./sahur_mcp

EXPOSE 8020

CMD ["uvicorn", "sahur_mcp.main:app", "--host", "0.0.0.0", "--port", "8020", "--reload"]
