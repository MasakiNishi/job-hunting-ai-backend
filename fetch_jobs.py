# Job Hunting AI Tool: fetch_jobs.py
# Members: Masaki Nishi, Christian McKinnon, Susan Joh, and Alexander Wong
# Project Partner: Professor Gates
# CS 467 Portfolio Project
#
# Description:
# This is a standalone Python script that executes the Data Collection Phase
# of the Job Hunting AI Web Tool. It uses a combination of http requests
# and the SerpApi to fetch jobs from Google and saves the results in
# google_listings.json. # Built in collaboration with Alex, from his
# file: scrape_googlejobs.py.
#
# Source:
# 1.) SerpApi Documentation - https://pypi.org/project/serpapi/

# Imports: requests, json, os, and concurrent futures
import requests
import json
import os
from dotenv import load_dotenv

# Used to fetch jobs in parallel to reduce probability of rate limiting
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load API_KEY variables from a env file
load_dotenv()


def fetch_job_query(api_key, job_type, num_listings):
    """A helper method used to fetch job listings. It takes in the api_key,
    the query, and the desired number of listings."""
    query_string = f'{job_type}'  # Defined in the main function below
    # From the SerpApi documentation, we use google_jobs for the engine
    params = {
        'api_key': api_key, 'engine': 'google_jobs', 'q': query_string,
        'num': num_listings}

    # Implement try / catch to follow best practices in case of rejection
    try:
        # Set the response using HTTP requests
        response = requests.get('https://serpapi.com/search',
                                params=params)
        response.raise_for_status()
        return response.json().get('jobs_results', [])
    # Catch any request-related exceptions and print error message
    except requests.exceptions.RequestException as error:
        print(f'Error fetching data due to: {error}')
        return []


def fetch_job_listings(api_key, job_types, num_listings):
    """The main function to fetch job listings which takes in the api_key,
    query, and num_listings. It calls the fetch_job_query helper method.
    It uses threading to handle multiple request and returns the listings
    as "job_list."""
    job_list = []
    # Use threading for multiple concurrent requests; call fetch_job_query
    # Max workers set to 10 for now to reduce frequent context switching
    with ThreadPoolExecutor(max_workers=10) as pool:
        threads = [pool.submit(fetch_job_query, api_key, job_type,
                               num_listings) for job_type in job_types]
        for threads in as_completed(threads):
            job_list.extend(threads.result())
    return job_list


def save_results_to_json(path, data):
    """A simple method to store the results of fetch_job_listings to a
    JSON file. It uses the os module for directory creation if is DNE."""
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Implement try / catch block in data fails to write
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=2)
    except IOError as error:
        print(f"Error writing to file '{path}' due to: {error}")


def main():
    """The main method which calls each of the methods above to store the
    results of fetch_job_listings in google_listings.json."""
    # API key should be hidden when pushed to GitHub
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("Error with API key.")
    # Here are the technical job types we would like to search for:
    job_types = [
        'Software Engineer', 'Data Analyst', 'Data Scientist',
        'Junior Developer', 'Product Manager', 'Internship',
        'Front-end Developer', 'Network Engineer', 'DevOps Engineer',
        'Cybersecurity Analyst', 'Technical Support', 'Cloud Engineer',
        'IT Manager', 'Database Administrator', 'Software Tester',
        'Systems Analyst', 'Game Developer', 'AI Research Scientist',
        'Full Stack Developer', 'Mobile App Developer', 'Blockchain Developer',
        'Embedded Systems Engineer', 'Robotics Engineer', 'Data Engineer',
        'Junior Intern', 'Data Intern', 'Technical Sales', 'UX Designer',
        'UI Designer', 'Intern', 'Bioinformatics', 'Remote', 'Hybrid'
    ]
    num_listings = 100  # Set the number of jobs listings to fetch
    # Assign the results of fetch_job_listings to job_listings
    job_listings = fetch_job_listings(api_key, job_types, num_listings)
    # Define the path
    path = 'json_files/google_listings.json'
    save_results_to_json(path, job_listings)
    # Print a success message to the console
    print('Job results updated in google_listings.json!')


if __name__ == '__main__':
    main()
