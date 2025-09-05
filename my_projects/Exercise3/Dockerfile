# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# System tools (curl valfritt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code (kopieras också men i dev mountas som volym via compose)
COPY . .

# Default env (kan override:as i compose)
ENV DATA_DIR=/app/Data \
    PYTHONUNBUFFERED=1

EXPOSE 8050

# Standardkommando för app-service (compose kan override:a kommandot)
CMD ["python", "ELT/dashboard.py"]