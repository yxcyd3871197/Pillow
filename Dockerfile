# Basis-Image auswählen
FROM python:3.9-slim

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Anwendung kopieren
COPY app.py app.py

# Exponiere den Port
EXPOSE 8080

# Startbefehl
CMD ["python", "app.py"]
