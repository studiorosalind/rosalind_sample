FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY sahur_batch/ ./sahur_batch

EXPOSE 8010

CMD ["uvicorn", "sahur_batch.main:app", "--host", "0.0.0.0", "--port", "8010", "--reload"]
