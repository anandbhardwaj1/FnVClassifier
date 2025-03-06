from flask import Flask, request, jsonify, render_template
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    try:
        data = request.get_json()
        image_url = data.get('image_url')
        print(image_url)
        if not image_url:
            return jsonify({'error': 'No image URL provided'}), 400

        # Just return Hello World instead of analyzing the image
        return jsonify({
            'success': True,
            'analysis': 'Hello World'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 