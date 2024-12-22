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

def process_image(heading, subheading, text, encoding):
    # Select a random image from the base-images folder
    image_files = [f for f in os.listdir('base-images') if f.endswith(('.jpg', '.jpeg', '.png'))]
    selected_image = random.choice(image_files)
    image_path = os.path.join('base-images', selected_image)

    # Open the image and prepare to draw on it
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Draw the text on the image
    draw.text((35, 300), heading, fill="white", font=ImageFont.load_default(130))
    draw.text((45, 500), subheading, fill="white", font=ImageFont.load_default(70))
    draw.text((55, 750), text, fill="white", font=ImageFont.load_default(50))

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
    heading = request.args.get('heading', '')
    subheading = request.args.get('subheading', '')
    text = request.args.get('text', '')
    encoding = request.args.get('encoding', 'binary')  # Check for encoding parameter

    return process_image(heading, subheading, text, encoding)

if __name__ == '__main__':
    app.run(debug=True)

