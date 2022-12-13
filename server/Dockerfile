FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["python", "main.py"]


