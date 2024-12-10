
# Claudio Perez
import sys
import json
from os import environ

import requests
from requests.auth import HTTPBasicAuth

def post_motion(filename):
    import os
    import requests

    # Environment variables for authentication and hostname
    username = os.getenv("IRIE_USERNAME")
    password = os.getenv("IRIE_PASSWORD")
    hostname = os.getenv("IRIE_HOSTNAME")

    if not all([username, password, hostname]):
        raise ValueError("Ensure all required environment variables and file path are set.")

    # API endpoint
    url = f"{hostname}/api/events/"

    # Open the file to upload
    with open(filename, "rb") as file:
        # Prepare the multipart-form data
        files = {
            "event_file": file
        }
        # Perform the POST request with Basic Auth
        response = requests.post(url, auth=(username, password), files=files)

    # Output the response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")


def post_evaluations(data):
    eval_data   = data["evaluation"]
    motion_data = data["motion_data"]
    eval_data.pop("event")
#   event_file = eval_data.pop("event_file")

    # Framework parameters
    # ----------------------------------
    username = environ["MOTION_API_USERNAME"]
    password = environ["MOTION_API_PASSWORD"]
    hostname = environ["MOTION_API_HOSTNAME"]

    # Setup API request
    # ----------------------------------
    headers = {
            # "Content-Type": "multipart/form-data",
    }

    files = {
        "evaluation": (None, json.dumps(eval_data)),
        "motion_data": (None, json.dumps(motion_data)),
#       "event_file": (event_file, open(event_file, "rb")),
    }

    # Perform request
    # ----------------------------------
    response = requests.post(
        hostname + "/api/events/",
        headers=headers,
        files=files,
        auth=HTTPBasicAuth(username, password)
    )

    print(response.content)


if __name__ == "__main__":
    filename = sys.argv[1]

    if filename.endswith(".zip"):
        post_motion(filename)
    
    else:
        with open(filename, "r") as f:
            data = json.load(f)["data"]

        for bridge in data:
            for event in bridge["events"]:
                post_evaluations(event)

