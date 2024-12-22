import time
from flask import Flask, request, send_file
import json
import os
import random
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/write-image', methods=['POST'])
def write_image():
    data = request.data
    json_data = json.loads(data)  # Parse JSON data
    heading = json_data.get('heading', '')
    subheading = json_data.get('subheading', '')
    text = json_data.get('text', '')

    # Select a random image from the base-images folder
    image_files = [f for f in os.listdir('base-images') if f.endswith(('.jpg', '.jpeg', '.png'))]
    selected_image = random.choice(image_files)
    image_path = os.path.join('base-images', selected_image)

    # Open the image and prepare to draw on it
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Define font (you may need to specify a path to a .ttf file)

    # Draw the text on the image
    draw.text((25, 300), heading, fill="white", font=ImageFont.load_default(67))
    draw.text((30, 500), subheading, fill="white", font=ImageFont.load_default(48))
    draw.text((75, 750), text, fill="white", font=ImageFont.load_default(35))

    # Save the modified image to a BytesIO buffer
    from io import BytesIO
    buffer = BytesIO()
    image.save(buffer, 'PNG')
    buffer.seek(0)

    # Send the image as a binary response directly from the buffer
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

