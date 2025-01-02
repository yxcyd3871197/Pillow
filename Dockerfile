# Basis-Image auswählen
FROM python:3.9-slim

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY app.py .

# Standard-Port und Startbefehl setzen
EXPOSE 8080
CMD ["python", "app.py"]
