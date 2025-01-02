# Basis-Image auswählen
FROM python:3.9-slim-buster

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Systemabhängigkeiten für Schriftarten installieren (wichtig!)
RUN apt-get update && apt-get install -y --no-install-recommends \
    fontconfig \
    ttf-freefont \
    && rm -rf /var/lib/apt/lists/*

# Abhängigkeiten installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Anwendung und Schriftarten kopieren
COPY app.py .
COPY fonts/ .

# Exponiere den Port
EXPOSE 8080

# Gunicorn verwenden (für die Produktion empfohlen)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
