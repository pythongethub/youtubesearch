
from flask import Flask, request, render_template_string, send_file
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        channel_ids, video_ids = youtube_search(search_query)
        channel_statistics = get_channel_stats(youtube, channel_ids)
        video_statistics = get_video_stats(youtube, video_ids)

        # Convert to DataFrames
        channel_data = pd.DataFrame(channel_statistics)
        video_data = pd.DataFrame(video_statistics)

        # Generate plots
        plt.figure(figsize=(10, 8))
        sns.barplot(x='channel_name', y='subscriber', data=channel_data.head(5))
        plt.xticks(rotation=45)
        plt.ylabel('Subscribers')
        plt.xlabel('Channel Name')
        plt.title('Top 5 Channels by Subscriber Count')
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')
    return '''
    <form method="post">
      Enter your search query: <input type="text" name="search_query">
      <input type="submit" value="Search">
    </form>
    '''

if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)
