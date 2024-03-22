from flask import Flask, request, jsonify
from multiple_api import API_KEYS, get_next_api_key, get_videos_data
import logging
import os
import pymongo

app = Flask(__name__)

# initialize logger for adding logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route('/api/videos', methods=['GET'])
def get_latest_videos():
    query = request.args.get('query')
    page_token = request.args.get('pageToken')

    if not query:
        error_message = "Query parameter 'query' is mising."
        logger.error(f"Error: {error_message}")
        return jsonify({"error": error_message}), 400
    
    for _ in range(len(API_KEYS)):
        # supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.
        api_key = get_next_api_key()
        logger.debug(f"Trying API key: {api_key}")
        data = get_videos_data(query, api_key, page_token)
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

             # Insert videos data into the MongoDB collection
            if videos:
                collection.insert_many(videos)

            # Convert ObjectId to string for each video
            for video in videos:
                if '_id' in video:
                    video['_id'] = str(video['_id'])    

            next_page_token = data.get('nextPageToken', None)
            return jsonify({'videos': videos, 'nextPageToken': next_page_token})     
            # return jsonify({'videos': videos})
        
        else:
            logger.error(f"Failed to fetch videos with API key: {api_key}")
    
    error_message = "All API keys exhausted or time limit exceeded."
    logger.error(f"error: {error_message}")
    return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    mongo_host = os.getenv("MONGODB_HOST")
    client = pymongo.MongoClient(mongo_host)
    logging.info("Connected to MongoDB")
    db = client["Mydb"]
    collection = db['youtube_api']
    app.run(debug=True)
