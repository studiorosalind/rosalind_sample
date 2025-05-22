FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY sahur_server/ ./sahur_server

EXPOSE 8000

CMD ["uvicorn", "sahur_server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
