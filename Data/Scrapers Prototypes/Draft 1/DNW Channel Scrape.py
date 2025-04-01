import os
import csv
import googleapiclient.discovery
import re

# Set your API key here
api_key = "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"

# Create a YouTube API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# Define the channel URL
channel_url = "https://www.youtube.com/@xvzf8147"  # Replace with the actual channel URL you want to fetch videos from

# Extract the channel ID from the URL using regular expressions
match = re.search(r"channel/([^/]+)", channel_url)

if match:
    channel_id = match.group(1)
    
    # Call the channels().list method to retrieve channel information
    channel_response = youtube.channels().list(
        id=channel_id,
        part="contentDetails"
    ).execute()

    # Check if the response contains any items
    if "items" in channel_response and len(channel_response["items"]) > 0:
        # Extract the playlist ID of the uploaded videos playlist
        playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Call the playlistItems().list method to retrieve videos from the playlist
        playlist_response = youtube.playlistItems().list(
            playlistId=playlist_id,
            part="snippet",
            maxResults=10  # You can change this to the number of results you want
        ).execute()

        # Initialize lists to store video URLs and titles
        video_urls = []
        video_titles = []

        # Iterate through the playlist results
        for playlist_item in playlist_response.get("items", []):
            video_url = f"https://www.youtube.com/watch?v={playlist_item['snippet']['resourceId']['videoId']}"
            video_title = playlist_item["snippet"]["title"]
            
            # Append to the respective lists
            video_urls.append(video_url)
            video_titles.append(video_title)

        # Use the channel name as the CSV filename (removing special characters)
        channel_name = channel_response["items"][0]["snippet"]["title"]
        csv_filename = f'{channel_name.replace(" ", "_").replace(":", "").replace("/", "")}_data.csv'

        # Create and write data to the CSV file
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Video Title', 'Video URL'])
            for i in range(len(video_urls)):
                writer.writerow([video_titles[i], video_urls[i]])

        print(f"CSV file '{csv_filename}' has been created with video titles and URLs from the channel.")
    else:
        print("No channel information found for the provided channel URL.")
else:
    print("Invalid channel URL format. Please provide a valid YouTube channel URL.")
