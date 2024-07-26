import os
from flask import Flask, request, jsonify
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)

# Initialize Vertex AI
PROJECT_ID = os.getenv('PROJECT_ID')
REGION = os.getenv('DEPLOY_REGION')
vertexai.init(project=PROJECT_ID, location=REGION)

# Load the model
MODEL_ID = os.getenv('MODEL_ID')
generative_multimodal_model = GenerativeModel(MODEL_ID)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# Just a test endpoint to check if the model is working
@app.route('/gemini', methods=['POST'])
def gemini():
    data = request.json
    input_text = data.get('text', '')

    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    response = generative_multimodal_model.generate_content([input_text])
    answer = response.text

    return jsonify({'answer': answer})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
