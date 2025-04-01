import os
import csv
import googleapiclient.discovery

# Set your API key here
api_key = "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"

# Create a YouTube API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# Define the query to search for videos
search_query = "Fashion"

# Call the search.list method to retrieve video information
search_response = youtube.search().list(
    q=search_query,
    type="video",
    part="id,snippet",
    maxResults=10  # You can change this to the number of results you want
).execute()

# Initialize lists to store video URLs and titles
video_urls = []
video_titles = []

# Iterate through the search results
for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        # Extract video URL and title
        video_url = f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
        video_title = search_result["snippet"]["title"]

        # Append to the respective lists
        video_urls.append(video_url)
        video_titles.append(video_title)

# Use the search query as the CSV filename (removing special characters)
csv_filename = f'{search_query.replace(" ", "_").replace(":", "").replace("/", "")}_data.csv'

# Create and write data to the CSV file
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Video Title', 'Video URL'])
    for i in range(len(video_urls)):
        writer.writerow([video_titles[i], video_urls[i]])

print(f"CSV file '{csv_filename}' has been created with video titles and URLs.")
