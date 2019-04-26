from django.conf import settings
import requests
import json


def send_to_slack_channel(channel, text):
    """Sending messages to Slack channels."""

    try:
        url = settings.SLACK_CHANNELS[channel]
    except KeyError:
        url = settings.SLACK_CHANNELS["default"]

    payload = {
        "text": text
    }
    if settings.DEBUG:
        print(text)
    else:
        requests.post(url=url, data=json.dumps(payload))
    return True
