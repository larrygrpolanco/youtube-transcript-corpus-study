import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Your YouTube Data API Key
API_KEY = "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"

# Building YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_youtube(query, max_pages=10, max_results=None, start_page_token=None, 
                   language="en", video_duration="short", published_after="2022-01-01T00:00:00-05:00", 
                   published_before=None, order="relevance", details_to_extract=None):
    """
    Search YouTube based on specified criteria and return video details.
    Incorporates error handling, pagination control, and flexibility in data extraction.
    """
    videos = []
    next_page_token = start_page_token
    total_results = 0

    for _ in range(max_pages):
        try:
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
                video_data = {}
                for detail in details_to_extract:
                    if detail == 'title':
                        video_data['Video Title'] = video['snippet']['title']
                    elif detail == 'id':
                        video_data['Video ID'] = video['id']
                    elif detail == 'publishDate':
                        video_data['Publish Date'] = video['snippet']['publishedAt']
                    elif detail == 'views':
                        video_data['Views'] = video['statistics'].get('viewCount', 0)
                    elif detail == 'duration':
                        video_data['Video Length'] = video['contentDetails']['duration'].replace("PT", "").replace("M", ":").replace("S", "")

                videos.append(video_data)

            total_results += len(video_response['items'])
            if max_results and total_results >= max_results:
                break

            # Updating the next_page_token for the next iteration
            next_page_token = search_response.get('nextPageToken')
            if not next_page_token:
                break

        except HttpError as e:
            print(f"An HTTP error occurred: {e.resp.status} {e.content}")
            break

    return videos

# Parameters (Can be modified)
search_query = "vlog"
max_pages = 5   # Number of pages to fetch, 50 max
details_to_extract = ['title', 'id', 'publishDate', 'views', 'duration']

# Fetching data
videos_data = search_youtube(search_query, max_pages=max_pages, details_to_extract=details_to_extract)

# Creating DataFrame
df = pd.DataFrame(videos_data)

# Exporting to CSV
csv_filename = f"{search_query}_youtube_videos.csv"
df.to_csv(csv_filename, index=False)
print(f"Data exported to {csv_filename}")

