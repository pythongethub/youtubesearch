from flask import Flask, render_template, request, jsonify
from threading import Thread
import time
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Initialize YouTube API
api_key = 'AIzaSyAg_dqXlgYhCRbvbEVY7jjV8qyJbJl6mOM'  # Replace with your actual API key
youtube = build('youtube', 'v3', developerKey=api_key)

# Your existing function definitions (youtube_search, get_channel_stats, get_video_stats)
# ...
def youtube_search(query, max_results=50):
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results,
        type='video',
        order='viewCount'
    ).execute()

    channels = []
    videos = []
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        channel_id = search_result['snippet']['channelId']
        videos.append(video_id)
        if channel_id not in channels:
            channels.append(channel_id)
    return channels, videos

def get_channel_stats(youtube, channel_ids):
    all_data = []
    for channel_id in channel_ids:
        request = youtube.channels().list(
            part='snippet, statistics', id=channel_id)
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            channel_info = response['items'][0]
            data = dict(
                channel_name=channel_info['snippet']['title'],
                channel_url=f'https://www.youtube.com/channel/{channel_id}',
                subscriber=int(channel_info['statistics']['subscriberCount']),
                views=int(channel_info['statistics']['viewCount']),
                total_videos=int(channel_info['statistics']['videoCount'])
            )
            all_data.append(data)
    return all_data

def get_video_stats(youtube, video_ids):
    video_data_list = []
    for video_id in video_ids:
        video_response = youtube.videos().list(
            part='snippet, statistics',
            id=video_id
        ).execute()

        if 'items' in video_response and len(video_response['items']) > 0:
            item = video_response['items'][0]
            stats = item['statistics']
            snippet = item['snippet']
            video_data_list.append({
                'channel_name': snippet['channelTitle'],
                'title': snippet['title'],
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
                'comments': int(stats.get('commentCount', 0))
            })
    return video_data_list

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    channel_ids, video_ids = youtube_search(query)
    video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids[:5]]
    return jsonify(video_urls)

if __name__ == '__main__':
    app.run(debug=True)
