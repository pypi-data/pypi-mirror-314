
# GitHub API Client

GitHub API Client is a Python library for interacting with the GitHub API. It simplifies the process of fetching data about repositories, commits, contributors, pull requests, and README content.

## Features
- Fetch repository information
- Fetch commits by the repository owner
- Fetch contributors to a repository
- Fetch open pull requests
- Fetch and decode the README file content
- Process commit data to check if commits were made today
- Fetch repositories of a specific user

## Installation
   ```bash
   pip install githubapiclient
   ```

## Usage

### Example Code
```python
from githubapiclient import GitHubAPIClient
import json

if __name__ == "__main__":
    # Replace with your GitHub token and repository owner
    token = "your_personal_access_token"
    repo_owner = "repository_owner"

    client = GitHubAPIClient(token, repo_owner)

    # Example: Get commit data for a specific repository
    repo_name = "your_repository_name"
    result = client.fetch_repo_info(repo_name)
    print(json.dumps(result, indent=4))
```

### Available Methods
- `fetch_repo_info(repo_name)` - Fetch details of a specific repository.
- `fetch_commits(repo_name)` - Fetch commits by the repository owner.
- `fetch_contributors(repo_name)` - Fetch contributors to a repository.
- `fetch_pull_requests(repo_name)` - Fetch open pull requests.
- `fetch_readme(repo_name)` - Fetch and decode the README file content.
- `fetch_user_repos()` - Fetch all repositories of the user.
- `process_commits(commits)` - Process commit data for today's commits.
- `load_commit_data(repo_name)` - Load and process all repository data.

## Configuration
- Replace the placeholder values for `token` and `repo_owner` in your script with actual values.
- You can generate a personal access token from GitHub under Developer Settings.

## Requirements
- Python 3.6+
- `requests` library

## License
This project is licensed under the MIT License.
