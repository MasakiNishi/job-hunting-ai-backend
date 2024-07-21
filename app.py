from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import pandas
import json

app = Flask(__name__)


@app.route('/')
def root():
    return 'AI Job Hunting Tool - Backend'

@app.route('/search', methods=['POST'])
def search_jobs():
    # get data from user input
    data = request.get_json()
    job_title = data.request.get('job_title')
    location = data.get('location')
    job_type = data.get('job_type')  # full/part-time, freelance, internship
    sector = data.get('sector')  # tech, finance, healthcare, etc
    experience = data.get('experience')  # length/level of work experience
    other = data.get('other')  # text input
    # more data as needed

    # check if all required inputs were entered
    if not job_title:  # add other categories as needed
        return jsonify({'error': 'Please provide both job title and location'}), 400
    
    job_listings = scrape_jobs(job_title, location, job_type, sector, experience, other)
    clean_job_listings = clean_data(job_listings)
    save_to_json(clean_job_listings, 'job_listings.json')

    return jsonify(clean_job_listings)

def scrape_jobs(job_title, location, job_type, sector, experience, other):
    # use job search sites and add info from data then input response to BeautifulSoup
    url = f'https://www.ajobsearchwebsite.com/jobs?1={job_title}'  # add extra info as needed
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # store results in 'jobs' list (change to dictionary?)
    jobs = []
    for job in soup.select('.job-listing'):
        title = job.select_one('.job-title').text
        # add company, location, summary, etc
        jobs.append({'title': title,
                     #'company': company,
                     #'location': location,
                     # etc
                     })
        
    return jobs

def clean_data(data):
    # need to implement
    pass

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
