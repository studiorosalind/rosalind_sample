FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# sahur-core editable install
COPY ../sahur-core ../sahur-core
RUN pip install -e ../sahur-core

COPY . .

EXPOSE 8010

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010", "--reload"]
