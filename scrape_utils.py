import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time


class ScraperUtils:
    def __init__(self, backoff_factor=0.3):
        self.backoff_factor = backoff_factor

    def load_user_criteria(self, filename='./text_JSON/user_answers.json'):
        """Load the user criteria from a JSON file."""
        with open(filename, 'r') as file:
            criteria = json.load(file)
        return criteria

    def send_get_request(self, url, retries=5):
        """Send a GET request to a URL with a retry mechanism."""
        print(f"Sending GET request to {url}")
        for i in range(retries):
            try:
                response = requests.get(url)
                response.raise_for_status()
                print("GET request successful")
                return response.text
            except requests.exceptions.HTTPError as e:
                print(f"HTTP error encountered: {e}")
                if response.status_code == 429:
                    wait_time = self.backoff_factor * (2 ** i)
                    print(f"Rate limit exceeded, retrying in {wait_time} seconds")
                    time.sleep(wait_time)
                else:
                    raise e
        raise requests.exceptions.HTTPError(
            f"Failed to fetch data from {url} after {retries} retries"
        )

    def parse_html(self, html_content):
        """Parse HTML content using BeautifulSoup."""
        return BeautifulSoup(html_content, "html.parser")

    def extract_job_ids(self, page_jobs):
        """Extract job IDs from job postings."""
        id_list = []
        for job in page_jobs:
            base_card_div = job.find("div", {"class": "base-card"})
            if base_card_div:
                job_id = base_card_div.get("data-entity-urn").split(":")[3]
                id_list.append(job_id)
        return id_list

    def save_to_json(self, data, filename):
        """Save data to a JSON file."""
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def convert_to_dataframe(self, data_list):
        """Convert a list of dictionaries to a pandas DataFrame."""
        print("Converting data to DataFrame")
        return pd.DataFrame(data_list)
