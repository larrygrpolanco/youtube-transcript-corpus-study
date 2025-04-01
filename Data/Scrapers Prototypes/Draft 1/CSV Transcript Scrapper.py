# Scrapper that creates transcripts from a CSV file

from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

# Ask the user for the CSV file containing video titles and links
csv_file = input("Enter the path to the CSV file: ")

# Read the CSV file into a DataFrame
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print("CSV file not found.")
    exit(1)

# Process the videos and save transcripts
for index, row in df.iterrows():
    video_title = row['Video Title']
    video_url = row['Video URL']

    video_id = video_url.replace('https://www.youtube.com/watch?v=', '')

    try:
        # Get the transcript for the current video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f'Error getting transcript for video "{video_title}": {str(e)}')
        continue  # Skip this video and continue with the next one

    # Create and open a text file for the current video with the custom name
    output_filename = f'{video_title}_transcript.txt'
    with open(output_filename, 'w', encoding='utf-8') as file:
        for x in transcript:
            sentence = x['text']
            file.write(f'{sentence}\n')

    print(f'Transcript for video "{video_title}" saved to {output_filename}')
