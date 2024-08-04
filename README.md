# Job Hunting AI Project Tool

**Members:** Masaki Nishi, Christian McKinnon, Susan Joh, Alexander Wong  
**Course:** Capstone Project for OSU CS 467

## Setting Up the Local Environment for job-hunting-ai-backend:

1. For detailed instructions on setting up your development environment, please refer to the README in the [Job Hunting AI Infra Repository](https://github.com/MasakiNishi/job-hunting-ai-infra).

2. **Copy the Local Environment File**:
   Execute `cp .env.local .env` in your terminal.

   This command creates a `.env` file from `.env.local`.

### Important Notes:

- **Securing Secrets**: Ensure that you do not commit and push the `.env.local` file with secret values to the repository. This precaution is why we rename `.env.local` to `.env`, where secrets are to be stored. The `.env` file should already be listed in the `.gitignore` to prevent it from being tracked by Git.

## Running the Google Jobs Scrape Script

This section provides instructions for running the Google Jobs scrape script inside a Docker container.

### Steps:

1. **Change API_KEY in .env file**

2. **Ensure Docker is Running:**

   - Make sure Docker is installed and running on your system.

3. **Start Containers:**

   - Use `docker-compose up` or the appropriate Docker command to start your containers.

4. **Find Container ID:**

   - Use the following command to list running containers and find the ID for the required container:
     ```bash
     docker ps
     ```

5. **Access Container Shell:**

   - Access the shell of the Docker container using its ID:
     ```bash
     docker exec -it [containerId] bash
     ```
     Replace `[containerId]` with the actual ID of your backend Docker container.

6. **Run the Script:**
   - Within the Docker container's shell, execute the script:
     ```bash
     python scrape_googlejobs.py
     ```

This will execute the script inside the Docker container, repopulate the `scrape_googlejobs.json` file with new results, and provide terminal output.
