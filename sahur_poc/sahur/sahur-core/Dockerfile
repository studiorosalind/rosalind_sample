FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# 개발용: editable install 지원
RUN pip install -e .

CMD ["python3"]
