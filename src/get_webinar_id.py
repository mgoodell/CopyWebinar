# get_webinar_id.py

import warnings
import requests
import os

warnings.simplefilter(action='ignore', category=FutureWarning)


def init():
    pass

# Fetch webinar data and get Webinar ID
def fetch_all_webinar_data(webinar_key, api_key, api_secret):
    # Disable proxy settings globally
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''

    url = 'https://api.webinar.net/v2/webinars'
    auth = (api_key, api_secret)
    page_index, page_size = 1, 50

    while True:
        response = requests.get(
            url,
            auth=auth,
            params={'pageIndex': page_index, 'pageSize': page_size},
            proxies={"http": None, "https": None}  # Disable proxy
        )
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

        data = response.json()
        registrants = data.get('webinars', [])
        if not registrants:
            print("No more data or unexpected data format.")
            return None

        for registrant in registrants:
            if registrant.get('webinarKey') == webinar_key:
                return registrant.get('id')

        if not data.get('hasMore', False):
            break
        page_index += 1

    return None
