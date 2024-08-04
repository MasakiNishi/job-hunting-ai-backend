# Job Hunting AI Project Tool

**Members:** Masaki Nishi, Christian McKinnon, Susan Joh, Alexander Wong  
**Course:** Capstone Project for OSU CS 467

## Setting Up the Local Environment for job-hunting-ai-backend:

1. For detailed instructions on setting up your development environment, please refer to the README in the [Job Hunting AI Infra Repository](https://github.com/MasakiNishi/job-hunting-ai-infra).

2. **Copy the Local Environment File**:
   Execute `cp .env.local .env` in your terminal.

   This command creates a `.env` file from `.env.local`.

## Using the Gemini API Locally

To use the Gemini API Locally, you need to configure certain environment variables. Follow these steps to set up:

1. **Modify the Environment Variables**:

   - Open the `.env` file in your preferred text editor.
   - Update the `PROJECT_ID` and `MODEL_ID` values to match our specific configurations. These values have been provided to you via MS Teams chat.

2. **Place the Service Account Key File**:
   Place the `service-account-key.json` file in the root directory. This file is necessary for authenticating with the Gemini API. This also have been provided to you via MS Teams chat.

### Important Notes:

- **Securing Secrets**: Ensure that you do not commit and push the `.env.local` file with secret values to the repository. This precaution is why we rename `.env.local` to `.env`, where secrets are to be stored. The `.env` file should already be listed in the `.gitignore` to prevent it from being tracked by Git.
- **Service Account Key File**: The `service-account-key.json` file contains sensitive authentication information. Do not share this file with anyone and ensure it is kept secure to prevent unauthorized access.
- **API Request Costs**: Be aware that each request to the Gemini API incurs costs. Please avoid sending large volumes of requests during development to manage costs effectively.


## For running the current LinkedIn web scrape script for Progress Report #3: *To be removed later

1. Set up local virtual environment by running `python3 -m venv env` in your terminal.

2. Activate the virtual environment: `source env/bin/activate`

3. Install all modules in requirements.txt file: `pip install -r requirements.txt`

3. **Run the file as a script**:

   - Display linkedin_jobs.json file
   - Run the script in terminal: `python scrape_linkedin.py`
   - linkedin_jobs.json will repopulate with new results along with terminal printout
