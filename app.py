from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

@app.route('/add_text', methods=['POST'])
def add_text():
    try:
        # Daten aus der Anfrage lesen
        data = request.json
        img_data = base64.b64decode(data['image'])
        text = data['text']

        # Bild aus den Base64-Daten laden
        with Image.open(io.BytesIO(img_data)) as img:
            draw = ImageDraw.Draw(img)

            # Text auf das Bild schreiben
            font = ImageFont.load_default()
            draw.text((10, 10), text, fill=(255, 255, 255), font=font)

            # Bild in Base64 umwandeln
            output = io.BytesIO()
            img.save(output, format="PNG")
            encoded_img = base64.b64encode(output.getvalue()).decode('utf-8')

        return jsonify({"image": encoded_img}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
