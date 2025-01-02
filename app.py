from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    data = request.json
    image_data = base64.b64decode(data['image'])
    text = data.get('text', 'Hello, Pillow!')

    with Image.open(io.BytesIO(image_data)) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((10, 10), text, fill="white", font=font)

        output = io.BytesIO()
        img.save(output, format="PNG")
        encoded_output = base64.b64encode(output.getvalue()).decode('utf-8')

    return jsonify({"processed_image": encoded_output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
