import os
import csv
from googleapiclient.discovery import build

# Set your API key
api_key = "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"

# Initialize the YouTube Data API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Define your search query
search_query = 'fashion'

# Specify the number of results per page and initial page token
max_results = 50  # You can adjust this based on your needs
next_page_token = None

# Create an empty list to store video data
video_data = []

try:
    while True:
        # Make a search request to the YouTube API
        search_response = youtube.search().list(
            q=search_query,
            type='video',
            maxResults=max_results,
            pageToken=next_page_token,
            part='id'
        ).execute()

        # Extract video IDs from the search results
        video_ids = [item['id']['videoId'] for item in search_response['items']]

        # Make a video list request to get details for each video
        videos_response = youtube.videos().list(
            id=','.join(video_ids),
            part='snippet,contentDetails,statistics'
        ).execute()

        # Iterate through video details and collect data
        for video in videos_response['items']:
            video_id = video['id']
            video_title = video['snippet']['title']
            publish_date = video['snippet']['publishedAt']
            views = video['statistics']['viewCount']
            comments_count = video['statistics'].get('commentCount', 0)
            
            # Check if captions are available
            captions_available = 'captions' in video['contentDetails']

            # Append video data to the list
            video_data.append([
                video_title,
                video_id,
                publish_date,
                views,
                comments_count,
                captions_available
            ])

        # Check for the next page token to continue pagination
        next_page_token = search_response.get('nextPageToken')

        if not next_page_token:
            break

except Exception as e:
    print(f"An error occurred: {str(e)}")

# Save the collected data to a CSV file
csv_file_name = 'youtube_video_data.csv'
with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Video Title', 'Video ID', 'Publish Date', 'Views', 'Comments Count', 'Captions Available'])
    csv_writer.writerows(video_data)

print(f'Data collection complete. Saved to {csv_file_name}.')