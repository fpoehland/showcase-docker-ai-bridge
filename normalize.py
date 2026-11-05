import cv2
import numpy as np
from flask import Flask, request, send_file
import io

app = Flask(__name__)

def process_image(image_bytes):
    # Bild aus Byte-Stream dekodieren
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return None

    # 1. In Graustufen umwandeln
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Rauschen reduzieren (Gaussian Blur)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Adaptiver Schwellenwert für perfektes Schwarz-Weiß (Binarisierung)
    # Ideal für Dokumente/Formeln unter wechselnden Lichtbedingungen (ESP32-CAM)
    normalized = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )

    # Bild wieder als PNG codieren
    _, buffer = cv2.imencode('.png', normalized)
    return io.BytesIO(buffer)

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}, 200

@app.route('/normalize', methods=['POST'])
def normalize():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400
    
    file = request.files['file']
    img_bytes = file.read()
    
    processed_io = process_image(img_bytes)
    if processed_io is None:
        return {"error": "Invalid image format"}, 400

    return send_file(processed_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
