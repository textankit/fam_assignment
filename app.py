from flask import Flask, request, jsonify
from multiple_api import API_KEYS, get_next_api_key, get_videos_data
import logging

app = Flask(__name__)

# initialize logger for adding logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route('/api/videos', methods=['GET'])
def get_latest_videos():
    query = request.args.get('query')
    if not query:
        error_message = "Query parameter 'query' is mising."
        logger.error(f"Error: {error_message}")
        return jsonify({"error": error_message}), 400
    
    for _ in range(len(API_KEYS)):
        # supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.
        api_key = get_next_api_key()
        logger.debug(f"Trying API key: {api_key}")
        data = get_videos_data(query, api_key)
        if data and 'error' not in data:
            videos = []
            for item in data['items']:
                video_data = {
                    'Video_title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_dataTime': item['snippet']['publishedAt'],
                    'video_Id': item['id']['videoId'],
                    'thumbnailUrl': item['snippet']['thumbnails']['default']['url']
                }
                videos.append(video_data)
            return jsonify({'videos': videos})
        else:
            logger.error(f"Failed to fetch videos with API key: {api_key}")
    
    error_message = "All API keys exhausted or time limit exceeded."
    logger.error(f"Error: {error_message}")
    return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)