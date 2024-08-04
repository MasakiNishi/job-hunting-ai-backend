# Job Hunting AI Tool: app.py
# Members: Masaki Nishi, Christian McKinnon, Susan Joh, and Alexander Wong
# Project Partner: Professor Gates
# CS 467 Portfolio Project
#
# Description:
# This Python file, app.py, is a Flask application that serves as the
# backend driver for the JHAI Web Tool. It sets up an API endpoint to
# take in user data via POST requests from HomePage.tsx on the frontend.
# In the submit() function, this user data and job listings gathered using
# the fetch_jobs.py file are passed into our job-recommender ML model. The
# top 5 results are then sent back to the frontend as a JSON response.
# Built in collaboration with Alex, from his file: scrape_googlejobs.py.
#
# Source:
# 1.) CORS Documentation: https://flask-cors.readthedocs.io/en/latest/api.html
#
# Should run on PORT  http://localhost:5001/

# Import the required modules: CORS enables frontend-backend communication
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import json
from model.recommender import job_recommender

# Load .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Create the user_list to store frontend input
user_list = []


# Set our API endpoint from the frontend to /api/submit
@app.route('/api/submit', methods=['POST'])
def submit():
    """A function that takes in user input from the frontend, converts
    the response to JSON format, appends that data to a Python list,
    then loads this list and the cleaned_listings.json file into our ML
    model, job_recommender(), and returns the output to the frontend."""
    # Use the os module to create a portable path for our JSON file
    clean_path = os.path.join(os.path.dirname(__file__),
                              'json_files', 'cleaned_listings.json')
    # Implement try / catch block when assigning the incoming response
    try:
        data = request.get_json()
        if data is None:
            raise ValueError('No user input found')
    except Exception as error:
        print(f'Error parsing data: {error}')
        return jsonify({'Error': f'Invalid JSON data: {error}'}), 400

    # Confirm receipt of the data
    print('\nSuccessfully received data from frontend.\n')

    # Append the received data to the user_list
    user_list.append(data)
    print(f'Data successfully written to list:, {user_list}\n')

    # Implement Try / Except block if unable to read cleaned_listings.json
    try:
        # Load Scraped Jobs From jobs.json (read mode)
        with open(clean_path, 'r') as jobFile:
            job_listings = json.load(jobFile)

        # Call the ML model with the most recent item in list in try/except
        parsed_rankings = job_recommender(user_list[-1], job_listings)
    except IOError as error:
        print(f'Error: {error}')
        return jsonify(
            {'Error': f'Error reading or running data: {error}'}), 500

    # Return the parsed rankings to the frontend and print success message
    print('Data successfully sent to frontend\n')
    return jsonify(parsed_rankings)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
