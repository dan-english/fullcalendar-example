from flask import Flask, request, render_template, render_template_string
from flask_cors import CORS, cross_origin

import json
import requests
import time
import os
import base64

from datetime import datetime, timezone, timedelta
from pprint import pprint

app = Flask(__name__, template_folder="./dist", static_folder="./dist/assets")
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
user_access_token = os.environ.get('ACCESS_TOKEN') + ':'
user_access_token_bytes = user_access_token.encode("ascii")

base64_bytes = base64.b64encode(user_access_token_bytes)
base64_user_access_token = base64_bytes.decode("ascii")

host_name =  os.environ.get('VITE_HOST_NAME')
host_email = os.environ.get('VITE_HOST_EMAIL_ADDRESS')
host_timezone = os.environ.get('VITE_HOST_TIME_ZONE')

host_primary_calendar = os.environ.get('PRIMARY_CALENDAR_ID')
host_alt_calendar = os.environ.get('ALT_CALENDAR_ID')
days=5
start_time = int(time.time())
end_time = start_time + (86400 * days)

print(start_time)


payload = {
    'duration_minutes': 30,
    'start_time': start_time,
    'end_time': end_time,
    'buffer':0,
    'interval_minutes': 30,
    'round_start': True,
    'free_busy': [],
    'emails': [host_email],
    'open_hours': [
        {
            'emails': [host_email],
            'days': [0,1,2,3,4],
            'timezone': host_timezone,
            'start': '09:00',
            'end': '12:00',
            'object_type': 'open_hours'
        },
        {
            'emails': [host_email],
            'days': [0, 1, 2, 3,4 ],
            'timezone': host_timezone,
            'start': '13:00',
            'end': '17:00',
            'object_type': 'open_hours'
        }
    ]
}


@app.route("/")
def main():
    return render_template("index.html", host=host_name)


@app.route('/send-confirmation', methods = ['POST'])
def confirmation_process():
    data = request.get_json()
    pprint(data)

    ##check we have an access token
    if not base64_user_access_token:
        return ["No Access Token"]

    calendar_event_response = create_calendar_event(data)

    print(data['config']['send_message_confirmation'])
    if data['config']['send_message_confirmation'] == 'True':
        send_message_response = send_message(data)
    else:
        send_message_response={'skip_confirmation_send':True}


    return {'event_response': calendar_event_response, 'send_response': send_message_response}


def send_message(data):
    message_template = """{% extends \"src/message_templates/"""+data['config']['template']+"""\" %}"""
    message_body = render_template_string(message_template, message_data=data)

    url = base_url + "/send"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+ base64_user_access_token,
    }
    payload = {
        "subject": "Meeting Confirmation With " + data['participant_name'],
        "to": [
            {
                "email": data['participant_email'],
                "name": data['participant_name']
            }
        ],
        "from": [
            {
                "email": data['host_email'],
                "name": data['host_name']
            }
        ],
        "body": message_body,
        "metadata": {
            "type": "scheduler_confirmation_message"
        }
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    json_response = json.loads(response.text)
    return json_response


## if using the host_alt_calendar and the participant is also the host expect to see the event twice on the google calendar
## (once as host, once as participant)
def create_calendar_event(data):

    meeting_duration = int(data['config']['duration'])
    start_time = datetime.fromtimestamp(int(data['selected_epoch']))
    end_time   = start_time + timedelta(minutes=meeting_duration)

    event_template = """{% extends \"src/event_templates/"""+data['config']['template']+"""\" %}"""
    event_description = render_template_string(event_template, message_data=data)

    url = base_url + "/events"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+ base64_user_access_token,
    }
    payload = {
        "title": "Scheduled Meeting With " + data['participant_name'],
        "calendar_id": host_alt_calendar,
        "visibility": "private",
        "busy": True,
        "participants": [
            {
                "name": data['participant_name'],
                "email": data['participant_email'],
                "status": "yes"
            }
        ],
        "description": event_description,
        "when": {
            "start_time": int(start_time.timestamp()),
            "end_time": int(end_time.timestamp()),
        },
        "location": "West Reservoir Centre, London N4 2HA",
        "conferencing": {
            "provider":"Google Meet",
            "details": {
                "url":"https://meet.google.com/bee-befz-uih",
                "pin":"115 911 603#",
                "phone":["+44 20 3956 5321"]
            }
        },
        "reminder_minutes":"[15]",
        "reminder_method":"popup"
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    json_response = json.loads(response.text)

    return json_response



### Updated request to accept configuration from the UI to alter the request payload (daysahead,duration)
@app.route("/availability-data", methods = ['POST'])
def get_availability_data():
    data = request.get_json()

    pprint(data)

    new_payload = payload
    new_payload['duration_minutes'] = data['duration']

    start_time = int(time.time())
    end_time = start_time + (86400 * data['lookahead_days'])
    new_payload['start_time'] = start_time
    new_payload['end_time'] = end_time

    pprint(new_payload)


    if not base64_user_access_token:
        return ["No Access Token"]

    url = base_url + "/calendars/availability"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+ base64_user_access_token
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(new_payload))
    json_response = json.loads(response.text)


    new_data = []
    days = []

    if 'time_slots' not in json_response:
        return json_response
    else:

        time_slots = json_response['time_slots']

        for slot in time_slots:
            b = time.strftime('%Y-%m-%d', time.localtime(slot['start']))
            slot['day'] = b
            if b not in days:
                days.append(b)
            new_data.append(slot)

    return {"time_slots": new_data, "days": days, "payload": new_payload}

