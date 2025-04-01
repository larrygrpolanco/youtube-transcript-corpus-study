import os
import csv
import googleapiclient.discovery

# Set your YouTube API key
api_key = "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"

# Create the YouTube API service
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

# Path to the CSV file containing Video IDs
csv_file_path = 'Analysis Sample Documentary/documentary_youtube_videos.csv'

# Create a directory to store the comments
output_directory = 'comments'
os.makedirs(output_directory, exist_ok=True)

# Read Video IDs from the CSV file
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        video_id = row['Video ID']

        # Get video title
        video_info = youtube.videos().list(part='snippet', id=video_id).execute()
        video_title = video_info['items'][0]['snippet']['title']

        # Get the top 50 video comments
        comments = []
        comments_response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=50
        ).execute()

        for comment in comments_response['items']:
            comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment_text)

        # Write comments to a text file
        output_file_path = os.path.join(output_directory, f'comments_{video_id}.txt')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Video Title: {video_title}\n")
            for comment in comments:
                output_file.write(f"{comment}\n")

        print(f"Top 50 comments for video '{video_title}' (ID: {video_id}) exported to {output_file_path}")
