from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import textwrap
import os

app = Flask(__name__)

# Schriftarten-Pfad anpassen
FONT_PATH = "fonts/"  # Relativer Pfad im Container

def process_image(request_data):
    # ... (Der Code zur Bildverarbeitung bleibt im Wesentlichen gleich)

    for layer in request_data.get("layers", []):
        try:
            if layer["type"] == "text":
                draw = ImageDraw.Draw(background_image)
                font_name = layer.get("font", "arial.ttf") # Standardfont
                font_path = os.path.join(FONT_PATH, font_name)
                font_size = int(layer.get("font_size", 30))
                # ... (Rest des Text-Layer-Codes)

                try:
                    font = ImageFont.truetype(font_path, font_size)
                except OSError:
                    print(f"Font not found at {font_path}. Using default font.") # Debugging
                    font = ImageFont.load_default()

            # ... (Rest des Layer-Codes)

        except Exception as e:
            print(f"Error processing layer: {e}") # Mehr Debugging
            return {"error": f"Error processing layer: {e}"}, 500

    # ... (Rest der Funktion)

@app.route('/process', methods=['POST'])
def handle_request():
    # ... (Bleibt gleich)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port) # Port aus Umgebungsvariable
