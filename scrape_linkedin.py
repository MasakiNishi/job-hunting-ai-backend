import json
import requests
from scrape_utils import ScraperUtils


class LinkedInScraper:
    def __init__(self):
        self.utils = ScraperUtils()

    def extract_job_details(self, job_id):
        """Extract job details from job ID."""
        job_url = f"https://www.linkedin.com/jobs/view/{job_id}"
        print(f"Fetching job details from {job_url}")
        job_response = self.utils.send_get_request(job_url)
        job_soup = self.utils.parse_html(job_response)

        job_post = {'job_url': job_url}
        job_post["job_title"] = self._extract_text(job_soup, "h3", {
            "class": "base-search-card__title"
        })
        job_post["company_name"] = self._extract_text(job_soup, "a", {
            "class": "topcard__org-name-link topcard__flavor--black-link"
        })
        job_post["time_posted"] = self._extract_text(job_soup, "span", {
            "class": "posted-time-ago__text topcard__flavor--metadata"
        })
        job_post["num_applicants"] = self._extract_text(job_soup, "span", {
            "class": (
                "num-applicants__caption topcard__flavor--metadata "
                "topcard__flavor--bullet"
            )
        })
        job_post["job_description"] = self._extract_text(job_soup, "div", {
            "class": "show-more-less-html__markup"
        })

        print(f"Fetched job details: {job_post}")
        return job_post

    def _extract_text(self, soup, tag, attrs):
        """Helper method to extract text from a BeautifulSoup object."""
        try:
            return soup.find(tag, attrs).text.strip()
        except AttributeError:
            return None

    def scrape_jobs(self, sector, output_filename='./text_JSON/linkedin_jobs.json', num_jobs=8):
        """Scrape job postings and save to a JSON file."""
        # Specify query for remote jobs (geoId=103644278) in the specified sector
        list_url = (
            "https://www.linkedin.com/jobs-guest/jobs/api/"
            "seeMoreJobPostings/search?keywords=" + sector
        )

        # Send a GET request to the URL and store the response
        list_data = self.utils.send_get_request(list_url)

        # Get the HTML, parse the response and find all list items (job postings)
        list_soup = self.utils.parse_html(list_data)
        page_jobs = list_soup.find_all("li")

        # Extract job IDs from the job postings
        id_list = self.utils.extract_job_ids(page_jobs)

        # Initialize an empty list to store job information
        job_list = []

        # Loop through the list of job IDs and get each job's details, limited to `num_jobs`
        for job_id in id_list[:num_jobs]:
            try:
                job_details = self.extract_job_details(job_id)
                job_list.append(job_details)
            except requests.exceptions.HTTPError as e:
                print(f"Failed to fetch job details for job ID {job_id}: {e}")
            except Exception as e:
                print(f"An error occurred while processing job ID {job_id}: {e}")

        # Load existing data
        try:
            with open(output_filename, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        # Append new job list to existing data
        existing_data.extend(job_list)

        # Save all job results into a JSON file
        with open(output_filename, 'w') as file:
            json.dump(existing_data, file, indent=2)

        print(f"Job data saved to {output_filename}")


if __name__ == "__main__":
    sectors = ["Technology", "Finance", "Education", "Healthcare", "Retail", "Energy"]
    scraper = LinkedInScraper()
    for sector in sectors:
        scraper.scrape_jobs(sector)
