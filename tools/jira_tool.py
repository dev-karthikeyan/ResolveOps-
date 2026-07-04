import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from jira import JIRA


class JiraTool:
    """
    Production-grade Jira client for ResolveOps.
    """

    def __init__(self):
        load_dotenv()

        self.server = os.getenv("JIRA_SERVER")
        self.email = os.getenv("JIRA_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")

        if not all([self.server, self.email, self.api_token]):
            raise ValueError("JIRA credentials not found in .env")

        self.client = JIRA(
            server=self.server,
            basic_auth=(self.email, self.api_token),
        )

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """
        Retrieve a Jira issue.
        """

        issue = self.client.issue(issue_key)

        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "status": issue.fields.status.name,
            "priority": issue.fields.priority.name,
            "assignee": (
                issue.fields.assignee.displayName
                if issue.fields.assignee
                else None
            ),
            "reporter": (
                issue.fields.reporter.displayName
                if issue.fields.reporter
                else None
            ),
            "created": issue.fields.created,
            "updated": issue.fields.updated,
        }

    def search_issues(
        self,
        jql: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search Jira issues using JQL.
        """

        issues = self.client.search_issues(
            jql,
            maxResults=limit,
        )

        results = []

        for issue in issues:

            results.append(
                {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": issue.fields.status.name,
                    "priority": issue.fields.priority.name,
                }
            )

        return results

    def add_comment(
        self,
        issue_key: str,
        comment: str,
    ) -> None:
        """
        Add a comment to an issue.
        """

        issue = self.client.issue(issue_key)

        self.client.add_comment(
            issue,
            comment,
        )

    def update_status(
        self,
        issue_key: str,
        transition_id: str,
    ) -> None:
        """
        Transition an issue to another status.
        """

        self.client.transition_issue(
            issue_key,
            transition_id,
        )

    def assign_issue(
        self,
        issue_key: str,
        account_id: str,
    ) -> None:
        """
        Assign an issue to a user.
        """

        self.client.assign_issue(
            issue_key,
            account_id,
        )