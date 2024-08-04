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
