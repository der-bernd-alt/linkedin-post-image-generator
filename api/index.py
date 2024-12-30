import time
from flask import Flask, request, send_file, render_template
import base64
import json
import os
import random
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__, template_folder=os.path.join('..', 'templates'))

@app.route('/test')
def home():
    return 'Hello, World!'

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/base64-decoder', methods=['GET'])
def base64_decode():
    return render_template('decoder.html')

def process_image(heading, subheading, text: list[str], encoding):
    # Select a random image from the base-images folder
    image_files = [f for f in os.listdir('base-images') if f.endswith(('.jpg', '.jpeg', '.png'))]
    selected_image = random.choice(image_files)
    image_path = os.path.join('base-images', selected_image)

    # Open the image and prepare to draw on it
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    text_positions = [
        (0.1, 0.6),  # heading
        (0.1, 0.7),  # subheading
        (0.1, 0.8)   # text
    ]
    font_sizes = [80, 60, 50]
    for i, (text, position, font_size) in enumerate(zip([heading, subheading, text], text_positions, font_sizes)):
        x, y = position

        text_color = "white"
        if i==1:
            text_color = "lightgray"

        if i==2:
            for part in text:
                draw.text((x * image.width, y * image.height), part, fill=text_color, font=ImageFont.load_default(font_size))
                y += 0.05
        else:
            draw.text((x * image.width, y * image.height), text, fill=text_color, font=ImageFont.load_default(font_size))

    # Save the modified image to a BytesIO buffer
    from io import BytesIO
    buffer = BytesIO()
    image.save(buffer, 'PNG')

    if encoding == 'base64':
        # Convert the image to base64 string with utf-8 encoding
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode('utf-8')
    else:
        # Send the image as a binary response directly from the buffer
        buffer.seek(0)
        return send_file(buffer, mimetype='image/png')

@app.route('/write-image', methods=['POST'])
def write_image():
    data = request.data
    json_data = json.loads(data)  # Parse JSON data
    heading = json_data.get('heading', '')
    subheading = json_data.get('subheading', '')
    text = json_data.get('text', '')
    encoding = json_data.get('encoding', 'binary')  # Check for encoding parameter

    return process_image(heading, subheading, text, encoding)

@app.route('/write-image-via-query', methods=['GET'])
def write_image_via_query():
    MAX_TEXT_LENGTH = 45
    
    heading = request.args.get('heading', '')
    subheading = request.args.get('subheading', '')
    text = request.args.get('text', '')
    lines = []
    current_line = ""
    for word in text.split():
        if len(current_line) + len(word) + 1 <= MAX_TEXT_LENGTH:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    text = lines
    encoding = request.args.get('encoding', 'binary')  # Check for encoding parameter

    print('Passing ', heading, subheading, text, encoding)
    return process_image(heading, subheading, text, encoding)

if __name__ == '__main__':
    app.run(debug=True)

