import os
import requests

class Slackbot:
    def __init__(self, slack_email):
        self.user_id = self._get_slack_user_id(slack_email)

    def _get_slack_user_id(self, user_email):
        """
        Fetch the Slack user ID based on the user's email.
        """
        response = requests.get(
            "https://slack.com/api/users.lookupByEmail",
            headers={"Authorization": f"Bearer {os.getenv('SLACK_TOKEN')}"},
            params={"email": user_email}
        )
        data = response.json()
        if data.get("ok"):
            return data["user"]["id"]
        else:
            raise Exception(f"Error fetching user ID: {data.get('error')}")

    def notify(self, message):
        """
        Send a direct message to a Slack user by their user ID.
        """
        user_id = self.user_id
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {os.getenv('SLACK_TOKEN')}", "Content-Type": "application/json"},
            json={"channel": user_id, "text": message}
        )
        data = response.json()
        if not data.get("ok"):
            raise Exception(f"Error sending message: {data.get('error')}")

