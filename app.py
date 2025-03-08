from flask import Flask, render_template, request, jsonify
import openai
from PIL import Image
import base64
import openapi
import os

from openapi import call_llm

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    # Convert image to Base64 for GPT processing
    img = Image.open(file)
    img.save("temp_image.jpg")

    with open("temp_image.jpg", "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    response = call_llm(img_base64)
    return response

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=4000, debug=True)
