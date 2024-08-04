from flask import Flask, request, jsonify
from flask_cors import CORS
from serpapi import GoogleSearch
from scrape_utils import ScraperUtils as utils
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve API_KEY from environment
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/submit', methods=['POST'])
def submit():
    user_responses = request.json

    # Create the query string based on the user responses
    query_string = utils.create_query(user_responses)

    # Define the parameters for the GoogleSearch API using the constructed query string
    params = {
        "api_key": API_KEY,
        "engine": "google_jobs",
        "google_domain": "google.com",
        "q": query_string
    }

    # Perform the search
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract the 'job_results' part
    job_results = results.get('jobs_results', [])

    # Save the extracted job results to a JSON file
    with open('./text_JSON/googlejob_results.json', 'w') as f:
        json.dump(job_results, f, indent=2)

    return jsonify({"message": "Job results saved successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
