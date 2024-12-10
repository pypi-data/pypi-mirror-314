import requests
from datetime import datetime
import json
import base64

class GitHubAPIClient:
    def __init__(self, token, repo_owner=None):
        self.token = token
        self.repo_owner = repo_owner
        self.base_url = f"https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}"
        }
        self.today_string = datetime.today().strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format

    def fetch_repo_info(self, repo_name):
        """Fetch repository information."""
        url = f"{self.base_url}/repos/{self.repo_owner}/{repo_name}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching repository info: {response.status_code} - {response.text}")
        return response.json()
    
    def fetch_language_statistics(self, repo_name):
        url = f"{self.base_url}/repos/{self.repo_owner}/{repo_name}/languages"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching language statistics: {response.status_code} - {response.text}")
        
        languages_data = response.json()
        total_bytes = sum(languages_data.values())
        
        # Calculate percentages for each language
        language_percentages = {
            language: round((bytes_count / total_bytes) * 100, 2)
            for language, bytes_count in languages_data.items()
        }
        return language_percentages


    def fetch_commits(self, repo_name):
        """Fetch commits by the repo owner."""
        url = f"{self.base_url}/repos/{self.repo_owner}/{repo_name}/commits"
        params = {
            'author': self.repo_owner,
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching commits: {response.status_code} - {response.text}")
        return response.json()

    def fetch_contributors(self, repo_name):
        """Fetch contributors to the repository."""
        url = f"{self.base_url}/repos/{self.repo_owner}/{repo_name}/contributors"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching contributors: {response.status_code} - {response.text}")
        return response.json()

    def fetch_pull_requests(self, repo_name):
        """Fetch open pull requests."""
        url = f"{self.base_url}/repos/{self.repo_owner}/{repo_name}/pulls"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching pull requests: {response.status_code} - {response.text}")
        return response.json()

    def fetch_readme(self, repo_name):
        """Fetch the README file content."""
        url = f"{self.base_url}/repos/{self.repo_owner}/{repo_name}/contents/README.md"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching README file: {response.status_code} - {response.text}")
        
        # GitHub API returns the file content as base64 encoded
        readme_data = response.json()
        readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        return readme_content

    def process_commits(self, commits):
        """Process commit data to check if there were commits today."""
        commit_data = []
        committed_today = False

        for commit in commits:
            commit_date = commit['commit']['author']['date']
            commit_message = commit['commit']['message']
            commit_date_str = commit_date.split("T")[0]  # Date in YYYY-MM-DD format

            if commit_date_str == self.today_string:
                committed_today = True

            commit_data.append({
                "message": commit_message,
                "date": commit_date_str
            })

        return {
            "committed_today": committed_today,
            "commits": commit_data
        }

    def fetch_user_repos(self):
        """Fetch repositories of the user."""
        url = f"{self.base_url}/users/{self.repo_owner}/repos"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching user repositories: {response.status_code} - {response.text}")
        return response.json()

    def load_commit_data(self, repo_name):
        """Load and process all data for a specific repository."""
        try:
            # Fetch data
            repo_info = self.fetch_repo_info(repo_name)
            commits = self.fetch_commits(repo_name)
            contributors = self.fetch_contributors(repo_name)
            pull_requests = self.fetch_pull_requests(repo_name)
            readme_content = self.fetch_readme(repo_name)

            # Process commit data
            commit_json = self.process_commits(commits)

            # Prepare the final JSON output
            result = {
                "repository_info": {
                    "name": repo_info.get("name"),
                    "description": repo_info.get("description"),
                    "owner": repo_info.get("owner", {}).get("login"),
                    "visibility": repo_info.get("private", False),
                    "created_at": repo_info.get("created_at"),
                },
                "commit_data": commit_json,
                "contributors": contributors,
                "open_pull_requests": [
                    {"title": pr["title"], "status": pr["state"], "created_at": pr["created_at"]} for pr in pull_requests
                ],
                "readme_content": readme_content  # Include the decoded README content
            }

            # Return the JSON output
            return json.dumps(result, indent=4)

        except Exception as e:
            return json.dumps({"error": str(e)})


