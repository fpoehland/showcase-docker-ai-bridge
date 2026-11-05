# Showcase: Docker AI-Bridge Normalization Engine

> **Privates Projekt / Proof of Concept**  
> Dieses Repository ist ein privates Hardware- & Cloud-Integrationsprojekt. 
> Es dient als praxisnaher Proof of Concept für die Containerisierung einer 
> Bildaufbereitungs-Pipeline (ESP32-CAM → Docker/OpenCV → TI-84 Plus).

---

## 💡 Übersicht & Motivation

Das Ziel des Projekts `AI-Bridge` ist die Automatisierung der Bildverarbeitung für eingebettete Systeme mit stark eingeschränkten Ressourcen. 

Ein ESP32-CAM Modul nimmt Rohbilder (z. B. Formeln oder Text) auf und überträgt diese per WLAN an eine Docker-basierte Microservice-Pipeline. Dort werden die Bilder mittels OpenCV entzerrt, gefiltert und binarisiert, um optimale Quelldaten für die anschließende Text- und Symbolerkennung (OCR) bereitzustellen. Das Ergebnis wird für die Rückgabe an einen TI-84 Plus Grafiktaschenrechner aufbereitet.

---

## 🏗 Systemarchitektur

```text
[ ESP32-CAM Modul ]
        │
        ▼ (HTTP POST / Multipart Upload)
┌────────────────────────────────────────────────────────┐
│ Docker Host (Ubuntu)                                   │
│                                                        │
│   [ Container: ai-bridge-normalize ]                   │
│   └── Flask REST API (Port 5000)                       │
│   └── OpenCV Engine (Blur -> Binarisierung -> PNG)     │
└────────────────────────────────────────────────────────┘
        │
        ▼ (Normalisiertes Schwarz-Weiß-Bild)
[ Pipeline Target: OCR & Variable Builder (.8xs / .8xp) ]
        │
        ▼ (Serial Link / Level-Shifter Board)
[ TI-84 Plus Target ]
```

## 🛠 Tech Stack

- **Operating System:** Ubuntu Linux

- **Containerization:** Docker / Buildx

- **Language & API:** Python 3.10, Flask

- **Image Processing:** OpenCV (Adaptive Thresholding, Gaussian Blur)

- **Version Control:** Git, GitHub CLI (`gh`)

## 🚀 Hands-On: Container lokal starten & testen

### 1. Requirements & Image Build

Bash

```
# Repository klonen
git clone git@github.com:fpoehland/showcase-docker-ai-bridge.git
cd showcase-docker-ai-bridge

# Docker Image bauen
docker build -t ai-bridge-normalize:latest .
```

### 2. Container ausführen

Bash

```
docker run -d -p 5000:5000 --name ai-bridge-normalize ai-bridge-normalize:latest
```

### 3. API-Endpunkte

- **Health Check:** `GET /health`

- **Image Normalization:** `POST /normalize`

Bash

```
# Beispiel-Test per cURL:
curl -X POST -F "file=@test_image.jpg" http://localhost:5000/normalize -o output.png
```

## 🛑 Projektstatus & Roadmap

Das Projekt befindet sich in der aktiven Weiterentwicklung.

- [x] **Core Engine:** Flask-basiertes Docker-Setup mit OpenCV-Verarbeitung (`normalize.py`)

- [x] **Build & Deployment:** Dockerfile & lokales Container-Build-Testing auf Ubuntu

- [x] **Versionierung:** GitHub-Repository & SSH-Integration aufgebaut

- [ ] **Hardware-Client:** C++ Firmware für ESP32-CAM Upload-Routine via HTTP POST

- [ ] **Hardware-Interface:** Integration des Chromalock PCB (ESP32-C3 Level-Shifter Board)

- [ ] **Downstream Pipeline:** Anbindung an OCR-Adapter (Tesseract / Groq REST-API)

*Entwickelt von Frank Pöhland im Rahmen von Recherchen zu IoT-Microservices und Linux-Systemintegration.*


