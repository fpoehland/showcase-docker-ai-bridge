FROM python:3.10-slim

# System-Abhängigkeiten für OpenCV installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python-Pakete installieren
RUN pip install --no-cache-dir flask opencv-python-headless numpy

# Anwendungs-Code kopieren
COPY normalize.py .

EXPOSE 5000

CMD ["python", "normalize.py"]
