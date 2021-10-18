import requests
import maya
import datetime
import random
from os import environ
from dotenv import load_dotenv
load_dotenv()

openingMessage = ["New Figma library version has been dropped!", "Ikan hiu makan pepaya, ada rilis baru buat library Figma",
                  "Ikan hiu suka ngaret, jangan lupa ada update!", "Jalan-jalan ke pasar baru, cek Figma-nya yu"]


def get_updates():
    FIGMA_PERSONAL_ACCESS_TOKEN = environ.get('FIGMA_PERSONAL_ACCESS_TOKEN')
    FIGMA_FILE_KEY = environ.get('FIGMA_FILE_KEY')
    FIGMA_API_URL = "https://api.figma.com/v1/files/" + FIGMA_FILE_KEY + "/versions"
    FIGMA_API_HEADERS = {'X-FIGMA-TOKEN': FIGMA_PERSONAL_ACCESS_TOKEN}

    r = requests.get(url=FIGMA_API_URL, headers=FIGMA_API_HEADERS)
    data = r.json()
    versions = data["versions"]

    def filter_function(x): return maya.parse(x['created_at']).datetime().date(
    ) == datetime.date.today() and x['description'] is not None and len(x['description']) > 0
    todays_versions = list(filter(filter_function, versions))
    if len(todays_versions) > 0:
        message = format_message(todays_versions)
        post_message(message)


def format_message(todays_versions):
    for version in todays_versions:
        label = version["label"]
        description = version["description"]
        message = "\n" + "**" + label + "**" + "\n" + "_" + \
            random.choice(openingMessage) + "_\n" + \
            "```\n" + description + "\n```"

    return message


def post_message(message):
    SLACK_TEAM_ID = environ.get('SLACK_TEAM_ID')
    SLACK_USER_ID = environ.get('SLACK_USER_ID')
    SLACK_CHANNEL_ID = environ.get('SLACK_CHANNEL_ID')
    SLACK_API_URL = "https://hooks.slack.com/services/" + \
        SLACK_TEAM_ID + "/" + SLACK_USER_ID + "/" + SLACK_CHANNEL_ID

    data = {"text": message}
    r = requests.post(url=SLACK_API_URL, json=data)
    print(message)


get_updates()
