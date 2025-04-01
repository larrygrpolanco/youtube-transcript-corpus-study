
# YouTube API documentation
# https://developers.google.com/youtube/v3/docs/search/list

import csv
import pandas as pd
from googleapiclient.discovery import build

# Your YouTube Data API Key
API_KEY = "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"

# Building YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_youtube(query, max_results=50, language="en", video_duration="any",
                   published_after=None, published_before=None, order="relevance"):
    """
    Search YouTube based on specified criteria and return video details.
    """
    # Searching YouTube
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        relevanceLanguage=language,
        type="video",
        videoDuration=video_duration,
        publishedAfter=published_after,
        publishedBefore=published_before,
        order=order
    ).execute()

    # Collecting video IDs
    video_ids = [item['id']['videoId'] for item in search_response['items']]

    # Getting video details
    video_response = youtube.videos().list(
        id=','.join(video_ids),
        part='snippet,statistics,contentDetails'
    ).execute()

    # Extracting required information
    videos = []
    for video in video_response['items']:
        videos.append({
            'Video Title': video['snippet']['title'],
            'Video ID': video['id'],
            'Publish Date': video['snippet']['publishedAt'],
            'Views': video['statistics'].get('viewCount', 0),
            'Video Length': video['contentDetails']['duration'].replace("PT", "").replace("M", ":").replace("S", "")
        })

    return videos

# Parameters (Can be modified)
search_query = "documentary"
page_limit = 50  # Pagination
count = 50      # Number of videos per page
language = "en" # Language
video_duration = "medium" # Video Duration
published_after = '2021-01-01T00:00:00Z' # Upload date
order = "viewCount" # Sorting

# Fetching data
videos_data = search_youtube(search_query, max_results=count, language=language,
                             video_duration=video_duration, order=order, published_after=published_after)

# Creating DataFrame
df = pd.DataFrame(videos_data)

# Exporting to CSV
df.to_csv(f"{search_query}_youtube_videos.csv", index=False)

