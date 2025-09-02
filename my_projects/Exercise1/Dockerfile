# Exercise2/Dockerfile
FROM python:3.11-slim

# Installera cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Sätt arbetskatalog i containern
WORKDIR /app

# Kopiera in hela Exercise2 (eftersom du bygger i den mappen)
COPY . .

# Installera Python-paket (filen ligger i /app/requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Se till att bash-scriptet är körbart
RUN chmod +x scripts/release_pokemons.sh

# Kopiera in cron-jobbet (filen ska finnas lokalt i Exercise2/cron/poketasks)
COPY cron/poketasks /etc/cron.d/poketasks
RUN chmod 0644 /etc/cron.d/poketasks && crontab /etc/cron.d/poketasks
RUN touch /var/log/poketasks.log

# Starta cron och streama loggen
CMD ["sh", "-c", "cron && tail -f /var/log/poketasks.log"]