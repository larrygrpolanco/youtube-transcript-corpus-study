import os
import csv
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi

# Set your YouTube API key here
api_key = "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"

# Create a YouTube API client
def create_youtube_client(api_key):
    return googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# Function to search for videos based on a query
def search_videos(api_client, query, max_results=1000):
    all_results = []
    next_page_token = None
    
    while max_results > 0:
        search_response = api_client.search().list(
            q=query,
            type="video",
            part="id,snippet",
            maxResults=min(max_results, 50),  # Maximum allowed results per request is 50
            pageToken=next_page_token
        ).execute()

        items = search_response.get("items", [])
        all_results.extend(items)
        
        if "nextPageToken" in search_response:
            next_page_token = search_response["nextPageToken"]
        else:
            break

        max_results -= 50  # Decrease the remaining results count

    return all_results


# Function to retrieve video URLs and titles from search results
def get_video_info(search_results):
    video_urls = []
    video_titles = []

    for search_result in search_results:
        if search_result["id"]["kind"] == "youtube#video":
            video_url = f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
            video_title = search_result["snippet"]["title"]

            video_urls.append(video_url)
            video_titles.append(video_title)

    return video_urls, video_titles


# Function to save video data to a CSV file
def save_to_csv(video_titles, video_urls, query):
    csv_filename = f'{query.replace(" ", "_").replace(":", "").replace("/", "")}_data.csv'

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Video Title', 'Video URL'])
        for i in range(len(video_urls)):
            writer.writerow([video_titles[i], video_urls[i]])

    print(f"CSV file '{csv_filename}' has been created with video titles and URLs.")


# Function to download video transcripts
def download_transcripts(video_info, query):
    video_title = video_info['Video Title']
    video_url = video_info['Video URL']

    video_id = video_url.replace('https://www.youtube.com/watch?v=', '')

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f'Error getting transcript for video "{video_title}": {str(e)}')
        return False

    output_filename = f'{query}_{video_title}_transcript.txt'
    with open(output_filename, 'w', encoding='utf-8') as file:
        for x in transcript:
            sentence = x['text']
            file.write(f'{sentence}\n')

    print(f'Transcript for video "{video_title}" saved to {output_filename}')
    return True


# Main function
def main():
    query = "Insert Query"  # Your search query
    max_results = 100  # Number of results to retrieve

    youtube_client = create_youtube_client(api_key)
    search_results = search_videos(youtube_client, query, max_results)
    video_urls, video_titles = get_video_info(search_results)
    
    save_to_csv(video_titles, video_urls, query)

    for video_info in [{'Video Title': title, 'Video URL': url} for title, url in zip(video_titles, video_urls)]:
        download_transcripts(video_info, query)

if __name__ == "__main__":
    main()
