from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json

    # Overwrite the JSON file with the received data
    with open('./text_JSON/user_answers.json', 'w') as file:
        json.dump(data, file, indent=4)

    return jsonify({"message": "Data saved successfully"}), 200
