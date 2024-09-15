# get_webinar_info.py

import warnings
import requests
import os

warnings.simplefilter(action='ignore', category=FutureWarning)


def init():
    pass

# Fetch webinar data and get Webinar ID
def fetch_webinar_details(new_webinar_id, api_key, api_secret):
    # Disable proxy settings globally
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''

    url = f'https://api.webinar.net/v2/webinars/{new_webinar_id}'
    auth = (api_key, api_secret)

    try:
        response = requests.get(
            url,
            auth=auth,
            proxies={"http": None, "https": None}  # Disable proxy for both HTTP and HTTPS
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch webinar details. Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
