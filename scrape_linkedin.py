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

        try:
            job_post["job_title"] = job_soup.find(
                "h2", {
                    "class": (
                        "top-card-layout__title font-sans text-lg papabear:text-xl "
                        "font-bold leading-open text-color-text mb-0 topcard__title"
                    )
                }
            ).text.strip()
        except AttributeError:
            job_post["job_title"] = None

        try:
            job_post["company_name"] = job_soup.find(
                "a", {"class": "topcard__org-name-link topcard__flavor--black-link"}
            ).text.strip()
        except AttributeError:
            job_post["company_name"] = None

        try:
            job_post["time_posted"] = job_soup.find(
                "span", {"class": "posted-time-ago__text topcard__flavor--metadata"}
            ).text.strip()
        except AttributeError:
            job_post["time_posted"] = None

        try:
            job_post["num_applicants"] = job_soup.find(
                "span", {
                    "class": (
                        "num-applicants__caption topcard__flavor--metadata "
                        "topcard__flavor--bullet"
                    )
                }
            ).text.strip()
        except AttributeError:
            job_post["num_applicants"] = None

        try:
            job_post["job_description"] = job_soup.find(
                "div", {"class": "show-more-less-html__markup"}
            ).text.strip()
        except AttributeError:
            job_post["job_description"] = None

        print(f"Fetched job details: {job_post}")
        return job_post

    def scrape_jobs(self, criteria_filename='./text_JSON/user_answers.json',
                    output_filename='./text_JSON/linkedin_jobs.json', num_jobs=5):
        """Scrape job postings and save to a JSON file."""
        # Load the user criteria from user_responses.json
        criteria = self.utils.load_user_criteria(criteria_filename)

        # Specify query for remote jobs in Technology sector in the United States
        list_url = (
            "https://www.linkedin.com/jobs-guest/jobs/api/"
            "seeMoreJobPostings/search?keywords=Technology&location=United%20States&"
            "geoId=103644278"  # LinkedIn US remote job geoId
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
            job_details = self.extract_job_details(job_id)
            job_list.append(job_details)

        # Convert the job list to a DataFrame and save it to JSON
        jobs_df = self.utils.convert_to_dataframe(job_list)
        
        # Save to JSON without escape characters
        jobs_df.to_json(output_filename, orient='records', lines=True, force_ascii=False)
        print(f"Job data saved to {output_filename}")


if __name__ == "__main__":
    scraper = LinkedInScraper()
    scraper.scrape_jobs()
