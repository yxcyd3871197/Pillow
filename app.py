from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.json
        image_data = data['image']

        # Padding hinzufügen, falls nötig
        missing_padding = len(image_data) % 4
        if missing_padding:
            image_data += '=' * (4 - missing_padding)

        decoded_image = base64.b64decode(image_data)
        text = data.get('text', 'Hello, Pillow!')

        with Image.open(io.BytesIO(decoded_image)) as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            draw.text((10, 10), text, fill="white", font=font)

            output = io.BytesIO()
            img.save(output, format="PNG")
            encoded_output = base64.b64encode(output.getvalue()).decode('utf-8')

        return jsonify({"processed_image": encoded_output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
