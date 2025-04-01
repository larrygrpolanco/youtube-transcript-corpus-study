import csv
from googleapiclient.discovery import build

# Initialize YouTube API client
api_key = "INSERT YOUR YOUTUBE API KEY"
youtube = build('youtube', 'v3', developerKey=api_key)

def get_playlist_videos(playlist_id, max_results, language, video_duration, upload_date, sort_by):
    """
    Fetch videos from a YouTube playlist and return a list of video details.
    """
    videos = []
    page_token = None

    while True:
        try:
            request = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=max_results,
                pageToken=page_token
            )
            response = request.execute()

            video_ids = [item['snippet']['resourceId']['videoId'] for item in response['items']]
            
            video_request = youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(video_ids)
            )
            video_response = video_request.execute()

            for item in video_response['items']:
                duration = item['contentDetails']['duration']
                published_at = item['snippet']['publishedAt']
                if (language is None or item['snippet']['defaultAudioLanguage'] == language) and \
                   (upload_date is None or upload_date <= published_at) and \
                   (video_duration is None or duration >= video_duration):
                    videos.append({
                        'Video Title': item['snippet']['title'],
                        'Video ID': item['id'],
                        'Channel ID': item['snippet']['channelId'],
                        'Playlist ID': playlist_id,
                        'Description': item['snippet']['description'],
                        'Publish Date': item['snippet']['publishedAt'],
                        'Views': item['statistics']['viewCount'],
                        'Video Length': duration
                    })

            page_token = response.get('nextPageToken')
            if not page_token:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    if sort_by:
        videos.sort(key=lambda x: x[sort_by])

    return videos

def export_to_csv(data, filename='youtube_playlist_data.csv'):
    """
    Export video data to a CSV file.
    """
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# List of playlist IDs
playlist_ids = [ 
    
    "Playlist IDs..."
                
                ]  # Replace with actual playlist IDs
max_results = 50  # Pagination
language = None  # Filter by language
video_duration = None  # Filter by video duration
upload_date = None  # Filter by upload date
sort_by = 'Views'  # Sort by views

aggregated_data = []
video_ids_collected = set()  # To avoid duplicates

for playlist_id in playlist_ids:
    video_data = get_playlist_videos(playlist_id, max_results, language, video_duration, upload_date, sort_by)
    for video in video_data:
        if video['Video ID'] not in video_ids_collected:
            aggregated_data.append(video)
            video_ids_collected.add(video['Video ID'])

export_to_csv(aggregated_data)
print("Data exported successfully.")


# "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"
