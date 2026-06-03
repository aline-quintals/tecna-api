import requests


WEBHOOK_URL = "https://discord.com/api/webhooks/1511718011399307367/VjqdExLd7FbxCpAiJArOTuFW3TZNtgKk-0N1tXJQYtqSHO4_42_dgHA5EuNds4Ink3D8"


def send_discord_alert(message):

    payload = {
        "content": message
    }

    requests.post(
        WEBHOOK_URL,
        json=payload
    )