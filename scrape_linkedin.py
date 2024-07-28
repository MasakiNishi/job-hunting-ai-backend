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
        job_post["job_title"] = self._extract_text(job_soup, "h2", {
            "class": (
                "top-card-layout__title font-sans text-lg papabear:text-xl "
                "font-bold leading-open text-color-text mb-0 topcard__title"
            )
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

    def scrape_jobs(self, criteria_filename='./text_JSON/user_answers.json',
                    output_filename='./text_JSON/linkedin_jobs.json', num_jobs=8):
        """Scrape job postings and save to a JSON file."""
        # Load the user criteria from user_responses.json
        self.utils.load_user_criteria(criteria_filename)

        # Specify query for remote jobs (geoId=103644278) in Technology sector in the United States
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

        # **** Remove commented code eventually in main development branch ****
        # Convert the job list to a DataFrame and save it to JSON
        # jobs_df = self.utils.convert_to_dataframe(job_list)

        # Save to JSON without escape characters
        # jobs_df.to_json(output_filename, orient='records', lines=True, force_ascii=False)
        
        self.utils.save_to_json(job_list, output_filename)
        print(f"Job data saved to {output_filename}")


if __name__ == "__main__":
    scraper = LinkedInScraper()
    scraper.scrape_jobs()
