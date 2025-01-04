# Basis-Image auswählen (schlanke Version)
FROM python:3.9-slim-buster

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Systemabhängigkeiten für Schriftarten installieren (wichtig!) und unnötige Pakete entfernen
RUN apt-get update && apt-get install -y --no-install-recommends \
    fontconfig \
    ttf-freefont \
    libjpeg-dev \ # Für JPEG-Unterstützung in Pillow
    zlib1g-dev \ # Für weitere Bildformate
    && rm -rf /var/lib/apt/lists/*

# Pillow mit JPEG- und ZLIB-Unterstützung neu installieren
RUN pip uninstall -y Pillow
RUN CFLAGS="-I/usr/include" LDFLAGS="-L/usr/lib" pip install --no-cache-dir Pillow

# Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendung und Schriftarten kopieren
COPY app.py .
COPY fonts/ ./fonts

# Port freigeben
EXPOSE 8080

# Gunicorn konfigurieren (wichtig für Cloud Run)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
