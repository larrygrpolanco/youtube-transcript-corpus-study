import os
import csv
from googleapiclient.discovery import build

# GARBAGE
def get_api_client():
    # Set your API key
    api_key = "AIzaSyD78b6sIkIkXYZrKoaE3BZg4UcCOipzP04"
    # Initialize the YouTube Data API client
    return build('youtube', 'v3', developerKey=api_key) 

def fetch_video_data(youtube, search_query, max_results):
    video_data = []
    next_page_token = None
    try:
        while True:
            search_response = youtube.search().list(
                q=search_query,
                type='video',
                maxResults=max_results,
                pageToken=next_page_token,
                part='id'
            ).execute()

            # [Rest of your data fetching and processing logic]

            if not next_page_token:
                break
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return video_data

def save_to_csv(file_name, data):
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Video Title', 'Video ID', 'Publish Date', 'Views', 'Comments Count', 'Captions Available', 'Description', 'Tags', 'Category'])
        csv_writer.writerows(data)

def main():
    youtube = get_api_client()
    search_query = 'fashion vlog'
    max_results = 50
    video_data = fetch_video_data(youtube, search_query, max_results)
    save_to_csv('youtube_video_data.csv', video_data)
    print('Data collection complete.')

if __name__ == "__main__":
    main()
