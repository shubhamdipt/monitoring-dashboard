from django.conf import settings
import requests
import json


def send_to_slack_channel(url, text):
    """Sending messages to Slack channels."""

    payload = {
        "text": text
    }
    if settings.DEBUG:
        print(text)
    else:
        requests.post(url=url, data=json.dumps(payload))
    return True
