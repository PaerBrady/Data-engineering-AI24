FROM python:3.11-slim

# Bättre dev-upplevelse
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Vanliga byggverktyg (valfritt men ofta bra)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installera beroenden om du har några
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt || true

# OBS: Vi kopierar inte in src här – den bind-mountas via compose
