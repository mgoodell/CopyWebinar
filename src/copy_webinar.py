# copy_webinar.py

from flask import session
import warnings
import requests

warnings.simplefilter(action='ignore', category=FutureWarning)


def init():
    pass

# Function to copy the webinar
def webinar_copy(webinar_id, api_key, api_secret, title, source, schedule_type, schedule_start, schedule_end,
                 time_zone, copy_media):

    url = f"https://api.webinar.net/v2/webinars/{webinar_id}/copy"
    auth = (api_key, api_secret)

    # Create the payload as per the API requirements
    payload = {
        "title": title,
        "language": "en_US",
        "source": source,
        "schedule": {
            "type": schedule_type,
            "start": schedule_start,
            "end": schedule_end,
            "timeZone": time_zone
        },
        "copyMedia": copy_media,
        "externalProperties": [
            {
                "name": "My Test External Property",
                "key": "myTestExternalProperty",
                "type": "text",
                "value": ["Property Value"]
            }
        ]
    }

    try:
        response = requests.post(url, auth=auth, json=payload)

        if response.status_code == 200:
            # Extract new webinar ID from the nested "webinar" object in the response
            new_webinar_id = response.json().get('webinar', {}).get('id')
            if new_webinar_id:
                session['new_webinar_id'] = new_webinar_id  # Store new webinar ID in session
                return True, "Webinar copied successfully."
            else:
                return False, "Webinar copied but failed to retrieve new ID."
        else:
            print(f"Failed to copy webinar. Status code: {response.status_code}, Response: {response.text}")
            return False, f"Failed to copy webinar: {response.text}"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False, f"An error occurred: {str(e)}"
