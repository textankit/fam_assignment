import requests
import logging

API_KEYS = ["AIzaSyDWIk_JVdqwUt4pawQHMP_nSD_vowpb0Ag","AIzaSyBdjv7ifiePpyt-Y6MuF8qog_3_r5Wt7_4"]
api_key_count = 0

# initialize logger for adding logs 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_next_api_key():
    global api_key_count
    api_key_count = (api_key_count + 1) % len(API_KEYS)
    return API_KEYS[api_key_count]

def get_videos_data(query, api_key):
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 10, # setting limit, it can be adjusted as per need
        'order': 'date',
        'key': api_key
    }
    response = requests.get('https://youtube.googleapis.com/youtube/v3/search', params=params)
    if response.status_code != 200:
        logger.error(f"error in getting videos. Status code: {response.status_code}")
        return None
    return response.json()
