import os
from typing import Optional

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackTool:
    """
    Production-grade Slack client for ResolveOps.
    """

    def __init__(self):
        load_dotenv()

        self.bot_token = os.getenv("SLACK_BOT_TOKEN")

        if not self.bot_token:
            raise ValueError("SLACK_BOT_TOKEN not found in .env")

        self.client = WebClient(token=self.bot_token)

    def send_message(
        self,
        channel_id: str,
        message: str,
    ) -> dict:
        """
        Send a message to a Slack channel.
        """

        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                text=message,
            )

            return {
                "success": True,
                "timestamp": response["ts"],
                "channel": response["channel"],
            }

        except SlackApiError as e:
            return {
                "success": False,
                "error": str(e),
            }

    def send_incident_summary(
        self,
        channel_id: str,
        summary: str,
    ) -> dict:
        """
        Send an incident summary.
        """

        return self.send_message(
            channel_id,
            f" Incident Summary\n\n{summary}",
        )

    def send_resolution(
        self,
        channel_id: str,
        resolution: str,
    ) -> dict:
        """
        Send the final incident resolution.
        """

        return self.send_message(
            channel_id,
            f" Incident Resolved\n\n{resolution}",
        )

    def upload_file(
        self,
        channel_id: str,
        file_path: str,
        title: Optional[str] = None,
    ) -> dict:
        """
        Upload a file to Slack.
        """

        try:
            response = self.client.files_upload_v2(
                channel=channel_id,
                file=file_path,
                title=title,
            )

            return {
                "success": True,
                "file_id": response["file"]["id"],
            }

        except SlackApiError as e:
            return {
                "success": False,
                "error": str(e),
            }
_slack_tool_instance = None


def _get_slack_tool() -> SlackTool:
    global _slack_tool_instance

    if _slack_tool_instance is None:
        _slack_tool_instance = SlackTool()

    return _slack_tool_instance


def send_slack_notification(message: str) -> dict:
    """
    Send a notification to the default Slack channel (from .env).
    Wrapper function used by slack_notification_agent.
    """

    channel_id = os.getenv("SLACK_CHANNEL_ID")

    if not channel_id:
        return {
            "success": False,
            "error": "SLACK_CHANNEL_ID not found in .env",
        }

    try:
        slack_tool = _get_slack_tool()

        return slack_tool.send_message(
            channel_id=channel_id,
            message=message,
        )

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }            

