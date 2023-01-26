from flask import Flask
from flask_cors import CORS, cross_origin

import json
import requests
import time
import os


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

###
# Pick your Nylas data-residency location
# US data-centre
base_url = 'https://api.nylas.com'
# EU data-centre
#base_url = 'https://ireland.api.nylas.com'
###

## add your Nylas access token - be sure to have the correct scopes/permissions on this token
user_token = os.environ.get('ACCESS_TOKEN')


@app.route("/")
def main():
    return "<p>main</p>"


@app.route("/availability")
def get_avail():
    start_time  = int(time.time())
    end_time = start_time+(86400 * 30)

    payload = {
        "duration_minutes": 30,
        'start_time': start_time,
        'end_time': end_time,
        "interval_minutes": 30,
        "round_start": True,
        'free_busy': [],
        'emails': [],
        'open_hours': []
    }

    url = base_url + "/calendars/availability"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+ user_token,
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    json_response = json.loads(response.text)

    time_slots = json_response['time_slots']

    new_data = []
    days = []
    for slot in time_slots:
        b = time.strftime('%Y-%m-%d', time.localtime(slot['start']))
        slot['day'] = b
        if b not in days:
            days.append(b)
        new_data.append(slot)

    return { "time_slots":new_data, "days":days}
