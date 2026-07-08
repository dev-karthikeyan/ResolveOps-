from langchain_core.tools import tool

from tools.github_tool import GitHubTool
from tools.confluence_tool import ConfluenceTool

github = GitHubTool()
confluence = ConfluenceTool()


def _safe_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as error:
        return {"error": str(error)}


@tool
def get_recent_commits(repository_name: str, limit: int = 10) -> list:
    """
    Get recent commits from a GitHub repository.
    """
    return _safe_call(github.get_recent_commits, repository_name, limit)


@tool
def get_pull_requests(repository_name: str, state: str = "all", limit: int = 10) -> list:
    """
    Get pull requests from a GitHub repository.
    """
    return _safe_call(github.get_pull_requests, repository_name, state, limit)


@tool
def search_github_issues(repository_name: str, keyword: str) -> list:
    """
    Search GitHub issues by keyword.
    """
    return _safe_call(github.search_issues, repository_name, keyword)


@tool
def search_github_pull_requests(repository_name: str, keyword: str) -> list:
    """
    Search GitHub pull requests by keyword.
    """
    return _safe_call(github.search_pull_requests, repository_name, keyword)


@tool
def get_file_content(repository_name: str, file_path: str, branch: str = "main") -> str:
    """
    Get the content of a specific file from a GitHub repository.
    """
    return _safe_call(github.get_file_content, repository_name, file_path, branch)


@tool
def search_confluence_pages(keyword: str, limit: int = 10) -> list:
    """
    Search Confluence documentation and runbooks by keyword.
    """
    return _safe_call(confluence.search_pages, keyword, limit)


@tool
def get_confluence_page_content(page_id: str) -> str:
    """
    Get the full content of a Confluence page.
    """
    return _safe_call(confluence.get_page_content, page_id)


investigation_tools = [
    get_recent_commits,
    get_pull_requests,
    search_github_issues,
    search_github_pull_requests,
    get_file_content,
    search_confluence_pages,
    get_confluence_page_content,
]