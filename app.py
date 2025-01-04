from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import textwrap

app = Flask(__name__)

def process_image(request_data):
    background_image_data = request_data.get("background_image")
    if not background_image_data:
        return {"error": "Missing background_image"}, 400

    try:
        background_image = Image.open(io.BytesIO(base64.b64decode(background_image_data))).convert("RGBA")
    except Exception as e:
        return {"error": f"Invalid background image: {e}"}, 400

    for layer in request_data.get("layers", []):
        try:
            if layer["type"] == "text":
                draw = ImageDraw.Draw(background_image)
                font_path = layer.get("font", "/usr/share/fonts/truetype/myfonts/YOUR_FONT.ttf")
                font_size = int(layer.get("font_size", 30))
                text_color = layer.get("color", "black")
                x = int(layer.get("x", 0))
                y = int(layer.get("y", 0))
                width = int(layer.get("width", background_image.width))
                height = int(layer.get("height", background_image.height))
                text = layer.get("text", "")
                align = layer.get("align", "left")

                try:
                    font = ImageFont.truetype(font_path, font_size)
                except OSError:
                    font = ImageFont.load_default()

                # Textumbruch und dynamische Schriftgrößenanpassung
                lines = textwrap.wrap(text, width=width / font.getsize(' ')[0])
                current_y = y

                for line in lines:
                    while draw.textsize(line, font=font)[0] > width and font_size > 1: # Schriftgröße nicht unter 1 verkleinern
                        font_size -= 1
                        try:
                            font = ImageFont.truetype(font_path, font_size)
                        except OSError:
                            font = ImageFont.load_default()
                            break

                    text_width, text_height = draw.textsize(line, font=font)
                    text_x = x
                    if align == "center":
                        text_x = x + (width - text_width) / 2
                    elif align == "right":
                        text_x = x + (width - text_width)
                    draw.text((text_x, current_y), line, fill=text_color, font=font)
                    current_y += text_height

            elif layer["type"] == "image":
                overlay_image_data = layer.get("image")
                if overlay_image_data:
                    overlay = Image.open(io.BytesIO(base64.b64decode(overlay_image_data))).convert("RGBA")
                    x = int(layer.get("x", 0))
                    y = int(layer.get("y", 0))
                    width = layer.get("width")
                    height = layer.get("height")
                    if width and height:
                        overlay = overlay.resize((int(width), int(height)), Image.ANTIALIAS)
                    background_image.paste(overlay, (x, y), overlay) # Transparenz berücksichtigen
        except Exception as e:
            return {"error": f"Error processing layer: {e}"}, 500

    output = io.BytesIO()
    background_image.save(output, format="PNG") # PNG für Transparenz
    encoded_output = base64.b64encode(output.getvalue()).decode('utf-8')
    return {"processed_image": encoded_output}, 200

@app.route('/process', methods=['POST'])
def handle_request():
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid JSON"}), 400
    return jsonify(process_image(request_data))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
