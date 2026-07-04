import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from github import Github


class GitHubTool:
    """
    Production-grade GitHub client for ResolveOps.
    """

    def __init__(self):
        load_dotenv()

        self.token = os.getenv("GITHUB_TOKEN")

        if not self.token:
            raise ValueError("GITHUB_TOKEN not found in .env")

        self.github = Github(self.token)

    def get_repository(self, repository_name: str):
        """
        Get a GitHub repository.

        Example:
        repository_name = "dev-karthikeyan/ResolveOps"
        """
        return self.github.get_repo(repository_name)

    def get_recent_commits(
        self,
        repository_name: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve recent commits from a repository.
        """

        repo = self.get_repository(repository_name)

        commits = []

        for commit in repo.get_commits()[:limit]:

            commits.append(
                {
                    "sha": commit.sha,
                    "author": (
                        commit.commit.author.name
                        if commit.commit.author
                        else "Unknown"
                    ),
                    "message": commit.commit.message,
                    "date": (
                        commit.commit.author.date.isoformat()
                        if commit.commit.author
                        else None
                    ),
                    "url": commit.html_url,
                }
            )

        return commits

    def get_pull_requests(
        self,
        repository_name: str,
        state: str = "all",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve pull requests.
        """

        repo = self.get_repository(repository_name)

        pull_requests = []

        for pr in repo.get_pulls(state=state)[:limit]:

            pull_requests.append(
                {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "author": pr.user.login if pr.user else "Unknown",
                    "created_at": pr.created_at.isoformat(),
                    "merged_at": (
                        pr.merged_at.isoformat()
                        if pr.merged_at
                        else None
                    ),
                    "url": pr.html_url,
                }
            )

        return pull_requests

    def get_issues(
        self,
        repository_name: str,
        state: str = "all",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve GitHub issues.
        """

        repo = self.get_repository(repository_name)

        issues = []

        for issue in repo.get_issues(state=state)[:limit]:

            # Skip pull requests
            if issue.pull_request is not None:
                continue

            issues.append(
                {
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "author": issue.user.login if issue.user else "Unknown",
                    "created_at": issue.created_at.isoformat(),
                    "url": issue.html_url,
                }
            )

        return issues

    def get_file_content(
        self,
        repository_name: str,
        file_path: str,
        branch: str = "main",
    ) -> str:
        """
        Retrieve file content from a repository.
        """

        repo = self.get_repository(repository_name)

        file = repo.get_contents(file_path, ref=branch)

        return file.decoded_content.decode("utf-8")

    def search_issues(
        self,
        repository_name: str,
        keyword: str,
    ) -> List[Dict[str, Any]]:
        """
        Search issues by keyword.
        """

        repo = self.get_repository(repository_name)

        results = []

        for issue in repo.get_issues(state="all"):

            if issue.pull_request is not None:
                continue

            text = f"{issue.title} {issue.body or ''}"

            if keyword.lower() in text.lower():

                results.append(
                    {
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "url": issue.html_url,
                    }
                )

        return results

    def search_pull_requests(
        self,
        repository_name: str,
        keyword: str,
    ) -> List[Dict[str, Any]]:
        """
        Search pull requests by keyword.
        """

        repo = self.get_repository(repository_name)

        results = []

        for pr in repo.get_pulls(state="all"):

            text = f"{pr.title} {pr.body or ''}"

            if keyword.lower() in text.lower():

                results.append(
                    {
                        "number": pr.number,
                        "title": pr.title,
                        "state": pr.state,
                        "url": pr.html_url,
                    }
                )

        return results