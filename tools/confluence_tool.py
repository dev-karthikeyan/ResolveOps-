import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from atlassian import Confluence


class ConfluenceTool:
    """
    Production-grade Confluence client for ResolveOps.
    """

    def __init__(self):
        load_dotenv()

        self.url = os.getenv("CONFLUENCE_URL")
        self.username = os.getenv("CONFLUENCE_EMAIL")
        self.api_token = os.getenv("CONFLUENCE_API_TOKEN")

        if not all([self.url, self.username, self.api_token]):
            raise ValueError("Confluence credentials not found in .env")

        self.client = Confluence(
            url=self.url,
            username=self.username,
            password=self.api_token,
        )

    def search_pages(
        self,
        keyword: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search Confluence pages.
        """

        pages = self.client.cql(
            f'text ~ "{keyword}"',
            limit=limit,
        )

        results = []

        for page in pages.get("results", []):

            results.append(
                {
                    "id": page["content"]["id"],
                    "title": page["content"]["title"],
                    "type": page["content"]["type"],
                }
            )

        return results

    def get_page_content(
        self,
        page_id: str,
    ) -> str:
        """
        Retrieve Confluence page content.
        """

        page = self.client.get_page_by_id(
            page_id,
            expand="body.storage",
        )

        return page["body"]["storage"]["value"]

    def get_page_title(
        self,
        page_id: str,
    ) -> str:
        """
        Retrieve page title.
        """

        page = self.client.get_page_by_id(page_id)

        return page["title"]