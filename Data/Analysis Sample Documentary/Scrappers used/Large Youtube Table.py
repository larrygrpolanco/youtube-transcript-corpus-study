import pandas as pd
from googleapiclient.discovery import build

# Your YouTube Data API Key
API_KEY = "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"

# Building YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_youtube(query, max_pages=10, language="en", video_duration="any",
                   published_after=None, published_before=None, order="relevance"):
    """
    Search YouTube based on specified criteria and return video details.
    Max results per page is 50 (maximum allowed by API).
    """
    videos = []
    next_page_token = None

    for _ in range(max_pages):
        # Searching YouTube
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=50,
            pageToken=next_page_token,
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
        for video in video_response['items']:
            videos.append({
                'Video Title': video['snippet']['title'],
                'Video ID': video['id'],
                'Publish Date': video['snippet']['publishedAt'],
                'Views': video['statistics'].get('viewCount', 0),
                'Video Length': video['contentDetails']['duration'].replace("PT", "").replace("M", ":").replace("S", "")
            })

        # Updating the next_page_token for the next iteration
        next_page_token = search_response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

# Parameters (Can be modified)
search_query = "Documentary"
max_pages = 10   # Number of pages to fetch, 50 max
language = "en"  # Language
video_duration = "medium" # Video Duration
order = "viewCount" # Sorting
# published_after = '2021-01-01T00:00:00Z' # Not being fetched  # Upload date

# Fetching data
videos_data = search_youtube(search_query, max_pages=max_pages, language=language,
                             video_duration=video_duration, order=order)

# Creating DataFrame
df = pd.DataFrame(videos_data)

# Exporting to CSV
df.to_csv(f"{search_query}_youtube_videos.csv", index=False)
